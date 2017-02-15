# grpcat

Arbitrary gRPC message sender - `grpcat` is `netcat` for gRPC. 

Usage
-----

Given a protobuf definition, `hello.proto`, compile it to python:

`$ python3 -m  grpc_tools.protoc  -I. --python_out=. --grpc_python_out=. hello.proto`

Given a service called `Hello` listening on `localhost` port `4444`, call the `GetHello`
RPC with a `GetHelloRequest` message parsed from text:

`$ cat get_hello_request.txt | grpcat.txt localhost 4444 /hello.Hello/GetHello GetHelloRequest`

The response from that request will be printed to `stdout`.
