# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/executor/events.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.executor import status_pb2 as eolymp_dot_executor_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='eolymp/executor/events.proto',
  package='eolymp.executor',
  syntax='proto3',
  serialized_options=b'Z7github.com/eolymp/contracts/go/eolymp/executor;executor',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1c\x65olymp/executor/events.proto\x12\x0f\x65olymp.executor\x1a\x1c\x65olymp/executor/status.proto\"=\n\x12StatusUpdatedEvent\x12\'\n\x06status\x18\x01 \x01(\x0b\x32\x17.eolymp.executor.StatusB9Z7github.com/eolymp/contracts/go/eolymp/executor;executorb\x06proto3'
  ,
  dependencies=[eolymp_dot_executor_dot_status__pb2.DESCRIPTOR,])




_STATUSUPDATEDEVENT = _descriptor.Descriptor(
  name='StatusUpdatedEvent',
  full_name='eolymp.executor.StatusUpdatedEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='eolymp.executor.StatusUpdatedEvent.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=140,
)

_STATUSUPDATEDEVENT.fields_by_name['status'].message_type = eolymp_dot_executor_dot_status__pb2._STATUS
DESCRIPTOR.message_types_by_name['StatusUpdatedEvent'] = _STATUSUPDATEDEVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StatusUpdatedEvent = _reflection.GeneratedProtocolMessageType('StatusUpdatedEvent', (_message.Message,), {
  'DESCRIPTOR' : _STATUSUPDATEDEVENT,
  '__module__' : 'eolymp.executor.events_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.executor.StatusUpdatedEvent)
  })
_sym_db.RegisterMessage(StatusUpdatedEvent)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
