# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/internal/factory_test1.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,google/protobuf/internal/factory_test1.proto\x12\x1fgoogle.protobuf.python.internal\"\xd5\x03\n\x0f\x46\x61\x63tory1Message\x12\x45\n\x0e\x66\x61\x63tory_1_enum\x18\x01 \x01(\x0e\x32-.google.protobuf.python.internal.Factory1Enum\x12\x62\n\x15nested_factory_1_enum\x18\x02 \x01(\x0e\x32\x43.google.protobuf.python.internal.Factory1Message.NestedFactory1Enum\x12h\n\x18nested_factory_1_message\x18\x03 \x01(\x0b\x32\x46.google.protobuf.python.internal.Factory1Message.NestedFactory1Message\x12\x14\n\x0cscalar_value\x18\x04 \x01(\x05\x12\x12\n\nlist_value\x18\x05 \x03(\t\x1a&\n\x15NestedFactory1Message\x12\r\n\x05value\x18\x01 \x01(\t\"P\n\x12NestedFactory1Enum\x12\x1c\n\x18NESTED_FACTORY_1_VALUE_0\x10\x00\x12\x1c\n\x18NESTED_FACTORY_1_VALUE_1\x10\x01*\t\x08\xe8\x07\x10\x80\x80\x80\x80\x02\")\n\x15\x46\x61\x63tory1MethodRequest\x12\x10\n\x08\x61rgument\x18\x01 \x01(\t\"(\n\x16\x46\x61\x63tory1MethodResponse\x12\x0e\n\x06result\x18\x01 \x01(\t*<\n\x0c\x46\x61\x63tory1Enum\x12\x15\n\x11\x46\x41\x43TORY_1_VALUE_0\x10\x00\x12\x15\n\x11\x46\x41\x43TORY_1_VALUE_1\x10\x01\x32\x97\x01\n\x0f\x46\x61\x63tory1Service\x12\x83\x01\n\x0e\x46\x61\x63tory1Method\x12\x36.google.protobuf.python.internal.Factory1MethodRequest\x1a\x37.google.protobuf.python.internal.Factory1MethodResponse\"\x00')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.protobuf.internal.factory_test1_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FACTORY1ENUM._serialized_start=638
  _FACTORY1ENUM._serialized_end=698
  _FACTORY1MESSAGE._serialized_start=82
  _FACTORY1MESSAGE._serialized_end=551
  _FACTORY1MESSAGE_NESTEDFACTORY1MESSAGE._serialized_start=420
  _FACTORY1MESSAGE_NESTEDFACTORY1MESSAGE._serialized_end=458
  _FACTORY1MESSAGE_NESTEDFACTORY1ENUM._serialized_start=460
  _FACTORY1MESSAGE_NESTEDFACTORY1ENUM._serialized_end=540
  _FACTORY1METHODREQUEST._serialized_start=553
  _FACTORY1METHODREQUEST._serialized_end=594
  _FACTORY1METHODRESPONSE._serialized_start=596
  _FACTORY1METHODRESPONSE._serialized_end=636
  _FACTORY1SERVICE._serialized_start=701
  _FACTORY1SERVICE._serialized_end=852
# @@protoc_insertion_point(module_scope)
