import argparse
import io
import socket
import sys
import threading

class WSGIHttpServer:

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    wait_queue_len = 5

    def __init__(self, host, port, app):
        self.app = app
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(self.wait_queue_len)

    def handle_requests_forever(self):
        # TODO: Make this asynchronous.
        while True:
            client_conn, _ = self.socket.accept()
            raw_request = client_conn.recv(1024)
            request = self.parse_request(raw_request)
            self.handle_one_request(request)

    def handle_one_request(self, request):
        pass

    def parse_request(self, request):
        pass

    def start_response(self, status, response_headers, exc_info=None):
        pass

    def finish_response(self, result):
        pass

    def set_environment(self):
        pass

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
