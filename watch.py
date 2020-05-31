import time
import logging
import os

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from logger import get_logger

log_default = get_logger(__name__)

class SimpleEventHandler(PatternMatchingEventHandler):

    def __init__(self, callback, *args, **kwargs):
        super(SimpleEventHandler, self).__init__(*args, **kwargs)
        self.callback = callback
    
    def catch_all_handler(self, event):
        self.callback()

    def on_moved(self, event):
        self.catch_all_handler(event)

    def on_created(self, event):
        self.catch_all_handler(event)

    def on_deleted(self, event):
        self.catch_all_handler(event)

    def on_modified(self, event):
        self.catch_all_handler(event)


def run_watchdog(path, dist_path, callback):
    log_default('Running watchdog at: %s', path, not_verbose=True)
    log_default('\tIgnoring changes at: %s', dist_path)
    event_handler = SimpleEventHandler(callback, ignore_patterns=[os.path.join(dist_path, '*')],
                                       ignore_directories=True)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
