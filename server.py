import logging

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from logger import get_logger


log_default = get_logger(__name__)

def init_handler(handler, directory):
    def inner(*args, **kwargs):
        return handler(directory=directory, *args, **kwargs)
    return inner

def run_server(port, path):
    handler = init_handler(SimpleHTTPRequestHandler, path)
    
    with TCPServer(("", port), handler) as httpd:
        log_default("Running server at localhost:%d", port, not_verbose=True)
        httpd.serve_forever()
