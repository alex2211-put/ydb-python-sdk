import abc
import enum
import logging
import threading
from typing import (
    Optional,
)

from . import base

from .. import _apis, issues, _utilities
from .._grpc.grpcwrapper import common_utils
from .._grpc.grpcwrapper import ydb_query as _ydb_query

from .transaction import BaseTxContext


logger = logging.getLogger(__name__)


class QuerySessionStateEnum(enum.Enum):
    NOT_INITIALIZED = "NOT_INITIALIZED"
    CREATED = "CREATED"
    CLOSED = "CLOSED"


class QuerySessionStateHelper(abc.ABC):
    _VALID_TRANSITIONS = {
        QuerySessionStateEnum.NOT_INITIALIZED: [QuerySessionStateEnum.CREATED],
        QuerySessionStateEnum.CREATED: [QuerySessionStateEnum.CLOSED],
        QuerySessionStateEnum.CLOSED: []
    }

    _READY_TO_USE = [
        QuerySessionStateEnum.CREATED
    ]

    @classmethod
    def valid_transition(cls, before: QuerySessionStateEnum, after: QuerySessionStateEnum) -> bool:
        return after in cls._VALID_TRANSITIONS[before]

    @classmethod
    def ready_to_use(cls, state: QuerySessionStateEnum) -> bool:
        return state in cls._READY_TO_USE


class QuerySessionState(base.IQuerySessionState):
    _session_id: Optional[str]
    _node_id: Optional[int]
    _attached: bool = False
    _settings: Optional[base.QueryClientSettings]
    _state: QuerySessionStateEnum

    def __init__(self, settings: base.QueryClientSettings = None):
        self._settings = settings
        self._state = QuerySessionStateEnum.NOT_INITIALIZED
        self.reset()

    def reset(self) -> None:
        self._session_id = None
        self._node_id = None
        self._attached = False

    @property
    def session_id(self) -> Optional[str]:
        return self._session_id

    def set_session_id(self, session_id: str) -> "QuerySessionState":
        self._session_id = session_id
        return self

    @property
    def node_id(self) -> Optional[int]:
        return self._node_id

    def set_node_id(self, node_id: int) -> "QuerySessionState":
        self._node_id = node_id
        return self

    @property
    def attached(self) -> bool:
        return self._attached

    def set_attached(self, attached: bool) -> "QuerySessionState":
        self._attached = attached

    def _check_invalid_transition(self, target: QuerySessionStateEnum):
        if not QuerySessionStateHelper.valid_transition(self._state, target):
            raise RuntimeError(f"Session could not be moved from {self._state.value} to {target.value}")

    def _change_state(self, target: QuerySessionStateEnum):
        self._check_invalid_transition(target)
        self._state = target

    def _check_session_ready_to_use(self):
        if not QuerySessionStateHelper.ready_to_use(self._state):
            raise RuntimeError(f"Session is not ready to use, current state: {self._state.value}")

    def _already_in(self, target):
        return self._state == target


def wrapper_create_session(rpc_state, response_pb, session_state: QuerySessionState, session):
    message = _ydb_query.CreateSessionResponse.from_proto(response_pb)
    issues._process_response(message.status)
    session_state.set_session_id(message.session_id).set_node_id(message.node_id)
    return session


def wrapper_delete_session(rpc_state, response_pb, session_state: QuerySessionState, session):
    message = _ydb_query.DeleteSessionResponse.from_proto(response_pb)
    issues._process_response(message.status)
    session_state.reset()
    session_state._change_state(QuerySessionStateEnum.CLOSED)
    return session


class BaseQuerySession(base.IQuerySession):
    _driver: base.SupportedDriverType
    _settings: Optional[base.QueryClientSettings]
    _state: QuerySessionState

    def __init__(self, driver: base.SupportedDriverType, settings: base.QueryClientSettings = None):
        self._driver = driver
        self._settings = settings
        self._state = QuerySessionState(settings)

    def _create_call(self):
        return self._driver(
            _apis.ydb_query.CreateSessionRequest(),
            _apis.QueryService.Stub,
            _apis.QueryService.CreateSession,
            wrap_result=wrapper_create_session,
            wrap_args=(self._state, self),
        )

    def _delete_call(self):
        return self._driver(
            _apis.ydb_query.DeleteSessionRequest(session_id=self._state.session_id),
            _apis.QueryService.Stub,
            _apis.QueryService.DeleteSession,
            wrap_result=wrapper_delete_session,
            wrap_args=(self._state, self),
        )

    def _attach_call(self):
        return self._driver(
            _apis.ydb_query.AttachSessionRequest(session_id=self._state.session_id),
            _apis.QueryService.Stub,
            _apis.QueryService.AttachSession,
        )

    def _execute_call(self, query: str, commit_tx: bool):
        request = base.create_execute_query_request(
            query=query,
            session_id=self._state.session_id,
            commit_tx=commit_tx
        )

        return self._driver(
            request,
            _apis.QueryService.Stub,
            _apis.QueryService.ExecuteQuery,
        )


class QuerySessionSync(BaseQuerySession):
    _stream = None

    def _attach(self):
        self._stream = self._attach_call()
        status_stream = _utilities.SyncResponseIterator(
            self._stream,
            lambda response: common_utils.ServerStatus.from_proto(response),
        )

        first_response = next(status_stream)
        if first_response.status != issues.StatusCode.SUCCESS:
            pass

        self._state.set_attached(True)
        self._state._change_state(QuerySessionStateEnum.CREATED)

        threading.Thread(
            target=self._chech_session_status_loop,
            args=(status_stream,),
            name="check session status thread",
            daemon=True,
        ).start()

    def _chech_session_status_loop(self, status_stream):
            try:
                for status in status_stream:
                    if status.status != issues.StatusCode.SUCCESS:
                        self._state.reset()
                        self._state._change_state(QuerySessionStateEnum.CLOSED)
            except Exception as e:
                pass


    def delete(self) -> None:
        if self._state._already_in(QuerySessionStateEnum.CLOSED):
            return

        self._state._check_invalid_transition(QuerySessionStateEnum.CLOSED)
        self._delete_call()
        self._stream.cancel()

    def create(self) -> None:
        if self._state._already_in(QuerySessionStateEnum.CREATED):
            return

        self._state._check_invalid_transition(QuerySessionStateEnum.CREATED)
        self._create_call()
        self._attach()

    def transaction(self, tx_mode: base.BaseQueryTxMode = None) -> base.IQueryTxContext:
        self._state._check_session_ready_to_use()

        return BaseTxContext(
            self._driver,
            self._state,
            self,
            tx_mode,
        )

    def execute(self, query: str, parameters=None):
        self._state._check_session_ready_to_use()

        stream_it = self._execute_call(query, commit_tx=True)

        return _utilities.SyncResponseIterator(
            stream_it,
            lambda resp: base.wrap_execute_query_response(rpc_state=None, response_pb=resp),
        )
