import argparse
import io
import socket
import sys
import time
import threading

class WSGIHttpServer:

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    wait_queue_len = 5

    def __init__(self, host, port, app):
        self.host = host
        self.server_name = socket.getfqdn(host)
        self.port = port
        self.app = app
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(self.wait_queue_len)

    def handle_requests_forever(self):
        # TODO: Make this asynchronous.
        while True:
            self.client_conn, _ = self.socket.accept()
            raw_request = self.client_conn.recv(1024)
            # FIXME: Don't parse the request here.
            request = self.parse_request(raw_request)
            self.handle_one_request(request)

    def handle_one_request(self, request):
        pass

    def parse_request(self, decoded_raw_request):
        request_line = decoded_raw_request.splitlines()[0].rstrip('\r\n')
        (self.method, self.request_path, self.http_server) = request_line.split()

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', time.asctime(time.localtime(time.time()))),
            ('Server', 'My fucking simple HTTP server 0.1.0')
        ]
        self.response_line_and_headers = (status, response_headers + server_headers)

    def finish_response(self, result):
        status, response_headers = self.response_line_and_headers
        response = f"HTTP/1.1 {status}\r\n"
        for header in response_headers:
            k, v = header
            response += f"{k}: {v}\r\n"
        response += "\r\n"
        for content in result:
            response += content.decode('utf-8')
        print(''.join(f'> {line}\n' for line in response.splitlines()))
        raw_response = response.encode()
        self.client_conn.sendall(raw_response)
        self.client_conn.close()

    def set_environment(self):
        env = {}
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(self.decoded_raw_request)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method
        env['PATH_INFO']         = self.path
        env['SERVER_NAME']       = self.server_name
        env['SERVER_PORT']       = str(self.port)
        return env

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A simple HTTP server that supports WSGI')
    parser.add_argument('-p', '--port', type=int, help='port number')
    parser.add_argument('module_name', type=str, help='module name of the program to run')
    parser.add_argument('start_func', type=str, help='starting function of the program to run')
    args = parser.parse_args()
    port = args.port
    module_name = args.module_name
    start_func = args.start_func
    print(f"HTTP server starts on http://127.0.0.1:{port}...")
