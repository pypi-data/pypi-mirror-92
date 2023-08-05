# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/keeper/keeper.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import http_pb2 as eolymp_dot_annotations_dot_http__pb2
from eolymp.annotations import scope_pb2 as eolymp_dot_annotations_dot_scope__pb2
from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='eolymp/keeper/keeper.proto',
  package='eolymp.keeper',
  syntax='proto3',
  serialized_options=b'Z3github.com/eolymp/contracts/go/eolymp/keeper;keeper',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1a\x65olymp/keeper/keeper.proto\x12\reolymp.keeper\x1a\x1d\x65olymp/annotations/http.proto\x1a\x1e\x65olymp/annotations/scope.proto\x1a\"eolymp/annotations/ratelimit.proto\"!\n\x11\x43reateObjectInput\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"!\n\x12\x43reateObjectOutput\x12\x0b\n\x03key\x18\x01 \x01(\t\"\"\n\x13\x44\x65scribeObjectInput\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x16\n\x14\x44\x65scribeObjectOutput\"\"\n\x13\x44ownloadObjectInput\x12\x0b\n\x03key\x18\x01 \x01(\t\"$\n\x14\x44ownloadObjectOutput\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32\xb5\x04\n\x06Keeper\x12\xb3\x01\n\x0c\x43reateObject\x12 .eolymp.keeper.CreateObjectInput\x1a!.eolymp.keeper.CreateObjectOutput\"^\x82\xe3\n\x17\x8a\xe3\n\x13keeper:object:write\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\x00@\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02-\"(/twirp/eolymp.keeper.Keeper/CreateObject:\x01*\x12\xba\x01\n\x0e\x44\x65scribeObject\x12\".eolymp.keeper.DescribeObjectInput\x1a#.eolymp.keeper.DescribeObjectOutput\"_\x82\xe3\n\x16\x8a\xe3\n\x12keeper:object:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00HB\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02/\"*/twirp/eolymp.keeper.Keeper/DescribeObject:\x01*\x12\xb7\x01\n\x0e\x44ownloadObject\x12\".eolymp.keeper.DownloadObjectInput\x1a#.eolymp.keeper.DownloadObjectOutput\"\\\x82\xe3\n\x16\x8a\xe3\n\x12keeper:object:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00HB\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02,\x12*/twirp/eolymp.keeper.Keeper/DownloadObjectB5Z3github.com/eolymp/contracts/go/eolymp/keeper;keeperb\x06proto3'
  ,
  dependencies=[eolymp_dot_annotations_dot_http__pb2.DESCRIPTOR,eolymp_dot_annotations_dot_scope__pb2.DESCRIPTOR,eolymp_dot_annotations_dot_ratelimit__pb2.DESCRIPTOR,])




_CREATEOBJECTINPUT = _descriptor.Descriptor(
  name='CreateObjectInput',
  full_name='eolymp.keeper.CreateObjectInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='eolymp.keeper.CreateObjectInput.data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=144,
  serialized_end=177,
)


_CREATEOBJECTOUTPUT = _descriptor.Descriptor(
  name='CreateObjectOutput',
  full_name='eolymp.keeper.CreateObjectOutput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='eolymp.keeper.CreateObjectOutput.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=179,
  serialized_end=212,
)


_DESCRIBEOBJECTINPUT = _descriptor.Descriptor(
  name='DescribeObjectInput',
  full_name='eolymp.keeper.DescribeObjectInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='eolymp.keeper.DescribeObjectInput.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=214,
  serialized_end=248,
)


_DESCRIBEOBJECTOUTPUT = _descriptor.Descriptor(
  name='DescribeObjectOutput',
  full_name='eolymp.keeper.DescribeObjectOutput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=250,
  serialized_end=272,
)


_DOWNLOADOBJECTINPUT = _descriptor.Descriptor(
  name='DownloadObjectInput',
  full_name='eolymp.keeper.DownloadObjectInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='eolymp.keeper.DownloadObjectInput.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=274,
  serialized_end=308,
)


_DOWNLOADOBJECTOUTPUT = _descriptor.Descriptor(
  name='DownloadObjectOutput',
  full_name='eolymp.keeper.DownloadObjectOutput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='eolymp.keeper.DownloadObjectOutput.data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=310,
  serialized_end=346,
)

DESCRIPTOR.message_types_by_name['CreateObjectInput'] = _CREATEOBJECTINPUT
DESCRIPTOR.message_types_by_name['CreateObjectOutput'] = _CREATEOBJECTOUTPUT
DESCRIPTOR.message_types_by_name['DescribeObjectInput'] = _DESCRIBEOBJECTINPUT
DESCRIPTOR.message_types_by_name['DescribeObjectOutput'] = _DESCRIBEOBJECTOUTPUT
DESCRIPTOR.message_types_by_name['DownloadObjectInput'] = _DOWNLOADOBJECTINPUT
DESCRIPTOR.message_types_by_name['DownloadObjectOutput'] = _DOWNLOADOBJECTOUTPUT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateObjectInput = _reflection.GeneratedProtocolMessageType('CreateObjectInput', (_message.Message,), {
  'DESCRIPTOR' : _CREATEOBJECTINPUT,
  '__module__' : 'eolymp.keeper.keeper_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.keeper.CreateObjectInput)
  })
_sym_db.RegisterMessage(CreateObjectInput)

CreateObjectOutput = _reflection.GeneratedProtocolMessageType('CreateObjectOutput', (_message.Message,), {
  'DESCRIPTOR' : _CREATEOBJECTOUTPUT,
  '__module__' : 'eolymp.keeper.keeper_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.keeper.CreateObjectOutput)
  })
_sym_db.RegisterMessage(CreateObjectOutput)

DescribeObjectInput = _reflection.GeneratedProtocolMessageType('DescribeObjectInput', (_message.Message,), {
  'DESCRIPTOR' : _DESCRIBEOBJECTINPUT,
  '__module__' : 'eolymp.keeper.keeper_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.keeper.DescribeObjectInput)
  })
_sym_db.RegisterMessage(DescribeObjectInput)

DescribeObjectOutput = _reflection.GeneratedProtocolMessageType('DescribeObjectOutput', (_message.Message,), {
  'DESCRIPTOR' : _DESCRIBEOBJECTOUTPUT,
  '__module__' : 'eolymp.keeper.keeper_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.keeper.DescribeObjectOutput)
  })
_sym_db.RegisterMessage(DescribeObjectOutput)

DownloadObjectInput = _reflection.GeneratedProtocolMessageType('DownloadObjectInput', (_message.Message,), {
  'DESCRIPTOR' : _DOWNLOADOBJECTINPUT,
  '__module__' : 'eolymp.keeper.keeper_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.keeper.DownloadObjectInput)
  })
_sym_db.RegisterMessage(DownloadObjectInput)

DownloadObjectOutput = _reflection.GeneratedProtocolMessageType('DownloadObjectOutput', (_message.Message,), {
  'DESCRIPTOR' : _DOWNLOADOBJECTOUTPUT,
  '__module__' : 'eolymp.keeper.keeper_pb2'
  # @@protoc_insertion_point(class_scope:eolymp.keeper.DownloadObjectOutput)
  })
_sym_db.RegisterMessage(DownloadObjectOutput)


DESCRIPTOR._options = None

_KEEPER = _descriptor.ServiceDescriptor(
  name='Keeper',
  full_name='eolymp.keeper.Keeper',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=349,
  serialized_end=914,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateObject',
    full_name='eolymp.keeper.Keeper.CreateObject',
    index=0,
    containing_service=None,
    input_type=_CREATEOBJECTINPUT,
    output_type=_CREATEOBJECTOUTPUT,
    serialized_options=b'\202\343\n\027\212\343\n\023keeper:object:write\352\342\n\014\365\342\n\000\000\000@\370\342\n\364\003\202\323\344\223\002-\"(/twirp/eolymp.keeper.Keeper/CreateObject:\001*',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DescribeObject',
    full_name='eolymp.keeper.Keeper.DescribeObject',
    index=1,
    containing_service=None,
    input_type=_DESCRIBEOBJECTINPUT,
    output_type=_DESCRIBEOBJECTOUTPUT,
    serialized_options=b'\202\343\n\026\212\343\n\022keeper:object:read\352\342\n\014\365\342\n\000\000HB\370\342\n\364\003\202\323\344\223\002/\"*/twirp/eolymp.keeper.Keeper/DescribeObject:\001*',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DownloadObject',
    full_name='eolymp.keeper.Keeper.DownloadObject',
    index=2,
    containing_service=None,
    input_type=_DOWNLOADOBJECTINPUT,
    output_type=_DOWNLOADOBJECTOUTPUT,
    serialized_options=b'\202\343\n\026\212\343\n\022keeper:object:read\352\342\n\014\365\342\n\000\000HB\370\342\n\364\003\202\323\344\223\002,\022*/twirp/eolymp.keeper.Keeper/DownloadObject',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_KEEPER)

DESCRIPTOR.services_by_name['Keeper'] = _KEEPER

# @@protoc_insertion_point(module_scope)
