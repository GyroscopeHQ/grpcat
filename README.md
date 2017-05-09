# grpcat

Arbitrary [gRPC](https://www.grpc.io) message sender - `grpcat` is `netcat` for gRPC. 

Usage
-----

Given a protobuf definition, `hello.proto`, compile it to python:

`$ python3 -m  grpc_tools.protoc  -I. --python_out=. --grpc_python_out=. hello.proto`

Given a service called `Hello` listening on `localhost` port `4444`, call the `GetHello`
RPC with a `GetHelloRequest` message parsed from text:

`$ cat get_hello_request.txt | grpcat.py localhost 4444 /hello.Hello/GetHello GetHelloRequest`

The response from that request will be printed to `stdout`.

Assumptions
-----------

`grpcat` assume Python 3. Additionally, at version `0.1` `grpcat` assumes that the compiled protobuf files are in the current working directory.

Testing
----
The test program `unit_tests.py` tests `grpcat.py` for the following functionality: valid command parsing from program arguments and a successful RPC server connection. 

Specifically whether the program

- reads in the command line arguments as excpected
- produces the appropriate error messages on too few or too many commands
- produces the appropriate error on an invalid target service format
- fails to make a connection to the RPC server
- succeeds in connecting to the RPC server

**Assumptions**
- compiled modules from hello.proto
- a get_hello_request.txt with a valid message, with the appropriate field specified in the `hello.proto`, for example `name:"Joe"`.

**Usage**

Run unit the unit tests the following way:

`$ python3 unit_tests.py`

The program will output the results of the unit tests. 


Copyright
---------

`grpcat` is distributed under the MIT License and is copyright 2017 [Gyroscope Software](https://www.gyroscope.cc).

grpcat includes contributions by Daniel Osváth Londoño.
