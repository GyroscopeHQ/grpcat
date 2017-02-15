# grpcat

Arbitrary [gRPC](https://www.grpc.io) message sender - `grpcat` is `netcat` for gRPC. 

Usage
-----

Given a protobuf definition, `hello.proto`, compile it to python:

`$ python3 -m  grpc_tools.protoc  -I. --python_out=. --grpc_python_out=. hello.proto`

Given a service called `Hello` listening on `localhost` port `4444`, call the `GetHello`
RPC with a `GetHelloRequest` message parsed from text:

`$ cat get_hello_request.txt | grpcat.txt localhost 4444 /hello.Hello/GetHello GetHelloRequest`

The response from that request will be printed to `stdout`.

Assumptions
-----------

`grpcat` assume Python 3. Additionally, at version `0.1` `grpcat` assumes that the compiled protobuf files are in the current working directory.


TODO
----

Tests and examples.

Copyright
---------

`grpcat` is distributed under the MIT License and is copyright 2017 [Gyroscope Software](https://www.gyroscope.cc).
