# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: draft/ydb_federated_query_v1.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ydb._grpc.v4.draft.protos import ydb_federated_query_pb2 as draft_dot_protos_dot_ydb__federated__query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"draft/ydb_federated_query_v1.proto\x12\x11\x46\x65\x64\x65ratedQuery.V1\x1a&draft/protos/ydb_federated_query.proto2\xd6\x0f\n\x15\x46\x65\x64\x65ratedQueryService\x12V\n\x0b\x43reateQuery\x12\".FederatedQuery.CreateQueryRequest\x1a#.FederatedQuery.CreateQueryResponse\x12V\n\x0bListQueries\x12\".FederatedQuery.ListQueriesRequest\x1a#.FederatedQuery.ListQueriesResponse\x12\\\n\rDescribeQuery\x12$.FederatedQuery.DescribeQueryRequest\x1a%.FederatedQuery.DescribeQueryResponse\x12_\n\x0eGetQueryStatus\x12%.FederatedQuery.GetQueryStatusRequest\x1a&.FederatedQuery.GetQueryStatusResponse\x12V\n\x0bModifyQuery\x12\".FederatedQuery.ModifyQueryRequest\x1a#.FederatedQuery.ModifyQueryResponse\x12V\n\x0b\x44\x65leteQuery\x12\".FederatedQuery.DeleteQueryRequest\x1a#.FederatedQuery.DeleteQueryResponse\x12Y\n\x0c\x43ontrolQuery\x12#.FederatedQuery.ControlQueryRequest\x1a$.FederatedQuery.ControlQueryResponse\x12\\\n\rGetResultData\x12$.FederatedQuery.GetResultDataRequest\x1a%.FederatedQuery.GetResultDataResponse\x12M\n\x08ListJobs\x12\x1f.FederatedQuery.ListJobsRequest\x1a .FederatedQuery.ListJobsResponse\x12V\n\x0b\x44\x65scribeJob\x12\".FederatedQuery.DescribeJobRequest\x1a#.FederatedQuery.DescribeJobResponse\x12\x65\n\x10\x43reateConnection\x12\'.FederatedQuery.CreateConnectionRequest\x1a(.FederatedQuery.CreateConnectionResponse\x12\x62\n\x0fListConnections\x12&.FederatedQuery.ListConnectionsRequest\x1a\'.FederatedQuery.ListConnectionsResponse\x12k\n\x12\x44\x65scribeConnection\x12).FederatedQuery.DescribeConnectionRequest\x1a*.FederatedQuery.DescribeConnectionResponse\x12\x65\n\x10ModifyConnection\x12\'.FederatedQuery.ModifyConnectionRequest\x1a(.FederatedQuery.ModifyConnectionResponse\x12\x65\n\x10\x44\x65leteConnection\x12\'.FederatedQuery.DeleteConnectionRequest\x1a(.FederatedQuery.DeleteConnectionResponse\x12_\n\x0eTestConnection\x12%.FederatedQuery.TestConnectionRequest\x1a&.FederatedQuery.TestConnectionResponse\x12\\\n\rCreateBinding\x12$.FederatedQuery.CreateBindingRequest\x1a%.FederatedQuery.CreateBindingResponse\x12Y\n\x0cListBindings\x12#.FederatedQuery.ListBindingsRequest\x1a$.FederatedQuery.ListBindingsResponse\x12\x62\n\x0f\x44\x65scribeBinding\x12&.FederatedQuery.DescribeBindingRequest\x1a\'.FederatedQuery.DescribeBindingResponse\x12\\\n\rModifyBinding\x12$.FederatedQuery.ModifyBindingRequest\x1a%.FederatedQuery.ModifyBindingResponse\x12\\\n\rDeleteBinding\x12$.FederatedQuery.DeleteBindingRequest\x1a%.FederatedQuery.DeleteBindingResponseBn\n\'tech.ydb.proto.draft.federated.query.v1ZCgithub.com/ydb-platform/ydb-go-genproto/draft/Ydb_FederatedQuery_V1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'draft.ydb_federated_query_v1_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\'tech.ydb.proto.draft.federated.query.v1ZCgithub.com/ydb-platform/ydb-go-genproto/draft/Ydb_FederatedQuery_V1'
  _FEDERATEDQUERYSERVICE._serialized_start=98
  _FEDERATEDQUERYSERVICE._serialized_end=2104
# @@protoc_insertion_point(module_scope)
