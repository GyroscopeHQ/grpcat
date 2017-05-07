# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import hello_pb2 as hello__pb2


class HelloStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetHello = channel.unary_unary(
        '/Hello/GetHello',
        request_serializer=hello__pb2.GetHelloRequest.SerializeToString,
        response_deserializer=hello__pb2.HelloReply.FromString,
        )


class HelloServicer(object):

  def GetHello(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_HelloServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetHello': grpc.unary_unary_rpc_method_handler(
          servicer.GetHello,
          request_deserializer=hello__pb2.GetHelloRequest.FromString,
          response_serializer=hello__pb2.HelloReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Hello', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
