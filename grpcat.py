import argparse
import fileinput
import grpc
import importlib
import sys
from google.protobuf import text_format

example_text = """
Example:

Given a protobuf definition, hello.proto, compile it to python:\n
$ python3 -m  grpc_tools.protoc  -I. --python_out=. --grpc_python_out=. hello.proto

Given a service called 'Hello' listening on localhost port 4444, call the 'GetHello'
RPC with a 'GetHelloRequest' message parsed from text:\n
$ cat get_hello_request.txt | grpcat.txt localhost 4444 /hello.Hello/GetHello GetHelloRequest

The response from that request will be printed to stdout.
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Arbitrary gRPC message sender.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("host", help="The host to connect to.")
    parser.add_argument("port", help="The port to connect to.")
    parser.add_argument(
        "rpc",
        help="The rpc to call on the target service in the form /<proto definition name>.<service>/<method>")
    parser.add_argument(
        "message_type",
        help="The message type being sent (eg, MyRpcRequest)")
    try:
        return parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


def run(args):
    # the gRPC channel we will connect to
    channel = grpc.insecure_channel(args.host + ":" + args.port)
    _, service, method = args.rpc.split('/')
    module_to_load, service = service.split('.')

    proto_module = importlib.import_module(module_to_load + "_pb2")
    grpc_module = importlib.import_module(module_to_load + "_pb2_grpc")

    service_stub_creator = getattr(grpc_module, service + "Stub")
    stub = service_stub_creator(channel)

    # Get the RPC to call
    rpc_to_call = getattr(stub, method)

    # Get the message factory
    message_factory = getattr(proto_module, args.message_type)

    message_text = ""
    message = message_factory()
    for line in fileinput.input(files=["-"]):
        message_text = message_text + line
    message_to_send = text_format.Merge(message_text, message)
    response = rpc_to_call(message_to_send)
    print(response.SerializeToString())

if __name__ == '__main__':
    args = parse_args()
    run(args)
