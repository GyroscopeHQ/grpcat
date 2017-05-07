from concurrent import futures
import time
import grpc
import hello_pb2
import hello_pb2_grpc

#  five minutes
_SERVER_TIME = 10 * 60


class Hello(hello_pb2_grpc.HelloServicer):

    def GetHello(self, request, context):
        return hello_pb2.HelloReply(message="name in message: %s\n" % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServicer_to_server(Hello(), server)
    server.add_insecure_port('[::]:4444')
    server.start()
    try:
        while True:
            time.sleep(_SERVER_TIME)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
