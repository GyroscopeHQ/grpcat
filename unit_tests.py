import sys
import os
from io import StringIO
import unittest
from unittest.mock import patch
import grpcat


class TestArgumentParsing(unittest.TestCase):
    """
        Test the argument parsing of grpcat.py
    """

    def test_expected_parse(self):
        """
            Check whether the grpcat parses valid argument input as expected.
        """

        test_args = [
            ['localhost', '4444', '/hello.Hello/GetHello',
             'GetHelloRequest'],
            ['localhost2', '5555', '/test2/Get-Test2',
             'GetRequest2'],
            ['host3', '333', '/hello.3/getTest3',
             'GetT3_Request'],
        ]

        expected_parse = [
            "Namespace(host='localhost', message_type='GetHelloRequest', "
            "port='4444', rpc='/hello.Hello/GetHello')",
            "Namespace(host='localhost2', message_type='GetRequest2', "
            "port='5555', rpc='/test2/Get-Test2')",
            "Namespace(host='host3', message_type='GetT3_Request', "
            "port='333', rpc='/hello.3/getTest3')"
        ]

        for i in range(len(test_args)):
            #  define sys args
            sys.argv[1:] = test_args[i]
            #  get return from the arg parse function
            retval = grpcat.parse_args()
            #  assertEqual
            self.assertEqual(expected_parse[i], str(retval))

    def test_arg_count_errors(self):
        """
            Check if the errors reported by grpcat are as expected.
        """

        # raw_input.return_value = input_data = "123"

        #  too many or few args
        test_args = [
            ['Too Few', '/hello.Hello/GetHello',
             'GetHelloRequest'],
            ['Too Many', '5555', '/test2/Get-Test2',
             'GetRequest2', 'extra']
        ]

        expected_errors = [
            "usage: unit_tests.py [-h] host port rpc message_type\n"
            "unit_tests.py: error: the following arguments are required:"
            " message_type\n",
            "usage: unit_tests.py [-h] host port rpc message_type\n"
            "unit_tests.py: error: unrecognized arguments: extra\n",
        ]

        #  save original out streams
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        #  throw away help output
        sys.stdout = out = open(os.devnull, "w")

        for i in range(len(test_args)):
            #  redirect error output for comparison
            sys.stderr = err = StringIO()

            sys.argv[1:] = test_args[i]
            #  catch the parse arg exception
            try:
                args = grpcat.parse_args()
                grpcat.run(args)
            except:
                pass

            self.assertEqual(err.getvalue(), expected_errors[i])

        out.close()
        #  resume normal output
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    #  mock file input
    @patch('fileinput.input')
    def test_arg_format_errors(self, fileinp):
        """
            Test if the correct formatting exception is raised when
            the target service is not in the form
            /<proto definition name>.<service>/<method>
        """

        text = open("get_hello_request.txt", "r")
        fileinp.return_value = text.read()
        text.close()

        test_args = [
            ['RPC Format Error', '/hello.HelloGetHello',
             'GetHelloRequest'],
            ['localhost', '4444', '/helloHello/GetHello',
             'GetHelloRequest'],
            ['localhost', '4444', '/hello-Hello/GetHello',
             'GetHelloRequest'],
            ['localhost', '4444', '\hello.Hello\GetHello',
             'GetHelloRequest']
        ]

        #  hide program errors and instructions
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = sys.stderr = out = open(os.devnull, "w")

        for t in test_args:
            sys.argv[1:] = t
            try:
                args = grpcat.parse_args()
                self.assertRaises(ValueError, grpcat.run(args))
            except:
                pass

        out.close()
        #  resume normal output
        sys.stdout = old_stdout
        sys.stderr = old_stderr


class MockRPCState(object):
    """
        A mock RPC State object to mock the response from a successful
        server connection. 
    """

    def SerializeToString(self):
        return ""


# mock the file input for the grpcat module
@patch('fileinput.input')
class TestRPCResponse(unittest.TestCase):
    """
        Tests to check server response.
    """

    @patch('grpc._channel._end_unary_response_blocking')
    def test_failed_connection(self, response, fileinp):
        """
            Test whether the connection to the RPC server fails, by mocking 
            the connection to fail. 
        """

        fail_message = ("<_Rendezvous of RPC that terminated with (StatusCode."
                        "UNAVAILABLE, Connect Failed)>")

        response.side_effect = Exception(fail_message)

        text = open("get_hello_request.txt", "r")
        fileinp.return_value = text.read()
        text.close()

        sys.argv[1:] = ['localhost', '4444', '/hello.Hello/GetHello',
                        'GetHelloRequest']

        args = grpcat.parse_args()

        try:
            grpcat.run(args)
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(fail_message, str(e))

    @patch('grpc._channel._end_unary_response_blocking')
    def test_successful_connection(self, response, fileinp):
        """
            Test whether the connection to the RPC server was successful. By
            mocking a successful response. 
        """

        response.return_value = MockRPCState()

        text = open("get_hello_request.txt", "r")
        fileinp.return_value = text.read()
        text.close()

        sys.argv[1:] = ['localhost', '4444', '/hello.Hello/GetHello',
                        'GetHelloRequest']

        args = grpcat.parse_args()

        try:
            grpcat.run(args)
            # there was a response from the server if
            # there is no exception
            self.assertTrue(True)
        except Exception:  # if there is an exception the connection has failed
            self.assertTrue(False)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
