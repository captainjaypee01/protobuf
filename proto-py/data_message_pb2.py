# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data_message.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import wp_global_pb2 as wp__global__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x64\x61ta_message.proto\x12\x19wirepas.proto.gateway_api\x1a\x0fwp_global.proto\"\x82\x02\n\rSendPacketReq\x12\x38\n\x06header\x18\x01 \x02(\x0b\x32(.wirepas.proto.gateway_api.RequestHeader\x12\x1b\n\x13\x64\x65stination_address\x18\x02 \x02(\r\x12\x17\n\x0fsource_endpoint\x18\x03 \x02(\r\x12\x1c\n\x14\x64\x65stination_endpoint\x18\x04 \x02(\r\x12\x0b\n\x03qos\x18\x05 \x02(\r\x12\x0f\n\x07payload\x18\x06 \x02(\x0c\x12\x18\n\x10initial_delay_ms\x18\x07 \x01(\r\x12\x18\n\x10is_unack_csma_ca\x18\x08 \x01(\x08\x12\x11\n\thop_limit\x18\t \x01(\r\"K\n\x0eSendPacketResp\x12\x39\n\x06header\x18\x01 \x02(\x0b\x32).wirepas.proto.gateway_api.ResponseHeader\"\xcb\x02\n\x13PacketReceivedEvent\x12\x36\n\x06header\x18\x01 \x02(\x0b\x32&.wirepas.proto.gateway_api.EventHeader\x12\x16\n\x0esource_address\x18\x02 \x02(\r\x12\x1b\n\x13\x64\x65stination_address\x18\x03 \x02(\r\x12\x17\n\x0fsource_endpoint\x18\x04 \x02(\r\x12\x1c\n\x14\x64\x65stination_endpoint\x18\x05 \x02(\r\x12\x16\n\x0etravel_time_ms\x18\x06 \x02(\r\x12\x18\n\x10rx_time_ms_epoch\x18\x07 \x02(\x04\x12\x0b\n\x03qos\x18\x08 \x02(\r\x12\x0f\n\x07payload\x18\t \x01(\x0c\x12\x14\n\x0cpayload_size\x18\n \x01(\r\x12\x11\n\thop_count\x18\x0b \x01(\r\x12\x17\n\x0fnetwork_address\x18\x0c \x01(\x04')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_message_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SENDPACKETREQ._serialized_start=67
  _SENDPACKETREQ._serialized_end=325
  _SENDPACKETRESP._serialized_start=327
  _SENDPACKETRESP._serialized_end=402
  _PACKETRECEIVEDEVENT._serialized_start=405
  _PACKETRECEIVEDEVENT._serialized_end=736
# @@protoc_insertion_point(module_scope)