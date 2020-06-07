import logging
import os

from livereload import Server

from logger import get_logger


log_default = get_logger(__name__)

def run_server(port, serve_path, watch_path, change_callback):

    log_default('Running server at: %d', port, not_verbose=True)
    
    server = Server()

    def ignore_fn(path):
        basename = os.path.basename(path)
        return serve_path in path or basename.startswith('.')

    server.watch(watch_path, change_callback, ignore=ignore_fn)
    
    server.serve(root=serve_path, port=port)
