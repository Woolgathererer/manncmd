from http.server import SimpleHTTPRequestHandler
from http.server import CGIHTTPRequestHandler
from http.server import ThreadingHTTPServer
from functools import partial
import contextlib
import sys
import os
from socket import socket


class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


def run(server_class=DualStackServer,
        handler_class=SimpleHTTPRequestHandler,
        port=8000,
        bind='0.0.0.0',
        cgi=False,
        directory=os.getcwd()):

    if cgi:
        handler_class = partial(CGIHTTPRequestHandler, directory=directory)
    else:
        handler_class = partial(SimpleHTTPRequestHandler, directory=directory)

    with server_class((bind, port), handler_class) as httpd:
        print(
            f"Serving HTTP on {bind} port {port} "
            f"(http://{bind}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    run()
