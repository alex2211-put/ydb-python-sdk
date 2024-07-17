from dataclasses import dataclass
import typing
from typing import Optional


# Workaround for good IDE and universal for runtime
if typing.TYPE_CHECKING:
    from ..v4.protos import ydb_query_pb2
else:
    from ..common.protos import ydb_query_pb2

from . import ydb_query_public_types as public_types

from .common_utils import (
    IFromProto,
    IToProto,
    IFromPublic,
    ServerStatus,
)

@dataclass
class CreateSessionResponse(IFromProto):
    status: Optional[ServerStatus]
    session_id: str
    node_id: int

    @staticmethod
    def from_proto(msg: ydb_query_pb2.CreateSessionResponse) -> "CreateSessionResponse":
        return CreateSessionResponse(
            status=ServerStatus(msg.status, msg.issues),
            session_id=msg.session_id,
            node_id=msg.node_id,
        )


@dataclass
class DeleteSessionResponse(IFromProto):
    status: Optional[ServerStatus]

    @staticmethod
    def from_proto(msg: ydb_query_pb2.DeleteSessionResponse) -> "DeleteSessionResponse":
        return DeleteSessionResponse(status=ServerStatus(msg.status, msg.issues))


@dataclass
class AttachSessionRequest(IToProto):
    session_id: str

    def to_proto(self) -> ydb_query_pb2.AttachSessionRequest:
        return ydb_query_pb2.AttachSessionRequest(session_id=self.session_id)


@dataclass
class TransactionMeta(IFromProto):
    tx_id: str

    @staticmethod
    def from_proto(msg: ydb_query_pb2.TransactionMeta) -> "TransactionMeta":
        return TransactionMeta(tx_id=msg.id)


@dataclass
class TransactionSettings(IFromPublic, IToProto):
    tx_mode: public_types.BaseQueryTxMode

    @staticmethod
    def from_public(tx_mode: public_types.BaseQueryTxMode) -> "TransactionSettings":
        return TransactionSettings(tx_mode=tx_mode)

    def to_proto(self) -> ydb_query_pb2.TransactionSettings:
        if self.tx_mode.name == 'snapshot_read_only':
            return ydb_query_pb2.TransactionSettings(snapshot_read_only=self.tx_mode.to_proto())
        if self.tx_mode.name == 'serializable_read_write':
            return ydb_query_pb2.TransactionSettings(serializable_read_write=self.tx_mode.to_proto())
        if self.tx_mode.name == 'online_read_only':
            return ydb_query_pb2.TransactionSettings(online_read_only=self.tx_mode.to_proto())
        if self.tx_mode.name == 'stale_read_only':
            return ydb_query_pb2.TransactionSettings(stale_read_only=self.tx_mode.to_proto())


@dataclass
class BeginTransactionRequest(IToProto):
    session_id: str
    tx_settings: TransactionSettings

    def to_proto(self) -> ydb_query_pb2.BeginTransactionRequest:
        return ydb_query_pb2.BeginTransactionRequest(
            session_id=self.session_id,
            tx_settings=self.tx_settings.to_proto(),
            )


@dataclass
class BeginTransactionResponse(IFromProto):
    status: Optional[ServerStatus]
    tx_meta: TransactionMeta

    @staticmethod
    def from_proto(msg: ydb_query_pb2.BeginTransactionResponse) -> "BeginTransactionResponse":
        return BeginTransactionResponse(
            status=ServerStatus(msg.status, msg.issues),
            tx_meta=TransactionMeta.from_proto(msg.tx_meta),
        )


@dataclass
class CommitTransactionResponse(IFromProto):
    status: Optional[ServerStatus]

    @staticmethod
    def from_proto(msg: ydb_query_pb2.CommitTransactionResponse) -> "CommitTransactionResponse":
        return CommitTransactionResponse(
            status=ServerStatus(msg.status, msg.issues),
        )


@dataclass
class RollbackTransactionResponse(IFromProto):
    status: Optional[ServerStatus]

    @staticmethod
    def from_proto(msg: ydb_query_pb2.RollbackTransactionResponse) -> "RollbackTransactionResponse":
        return RollbackTransactionResponse(
            status=ServerStatus(msg.status, msg.issues),
        )


@dataclass
class QueryContent(IFromPublic, IToProto):
    text: str
    syntax: Optional[str] = None

    @staticmethod
    def from_public(query: str) -> "QueryContent":
        return QueryContent(text=query)

    def to_proto(self) -> ydb_query_pb2.QueryContent:
        return ydb_query_pb2.QueryContent(text=self.text, syntax=self.syntax)


@dataclass
class TransactionControl(IToProto):
    begin_tx: Optional[TransactionSettings] = None
    commit_tx: Optional[bool] = None
    tx_id: Optional[str] = None

    def to_proto(self) -> ydb_query_pb2.TransactionControl:
        if self.tx_id:
            return ydb_query_pb2.TransactionControl(
                tx_id=self.tx_id,
                commit_tx=self.commit_tx,
            )
        return ydb_query_pb2.TransactionControl(
            begin_tx=self.begin_tx.to_proto(),
            commit_tx=self.commit_tx
        )


@dataclass
class ExecuteQueryRequest(IToProto):
    session_id: str
    query_content: QueryContent
    tx_control: TransactionControl
    concurrent_result_sets: Optional[bool] = False
    exec_mode: Optional[str] = None
    parameters: Optional[dict] = None
    stats_mode: Optional[str] = None

    def to_proto(self) -> ydb_query_pb2.ExecuteQueryRequest:
        return ydb_query_pb2.ExecuteQueryRequest(
            session_id=self.session_id,
            tx_control=self.tx_control.to_proto(),
            query_content=self.query_content.to_proto(),
            exec_mode=ydb_query_pb2.EXEC_MODE_EXECUTE,
            stats_mode=self.stats_mode,
            concurrent_result_sets=self.concurrent_result_sets,
            parameters=self.parameters,
        )
