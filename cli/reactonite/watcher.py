import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class reactonite_watcher():
    def __init__(self,
                 dir,
                 patterns="*",
                 ignore_patterns="",
                 ignore_directories=False,
                 case_sensitive=True,
                 recursive=True):
        self.dir = dir
        self.patterns = patterns
        self.ignore_patterns = ignore_patterns
        self.ignore_directories = ignore_directories
        self.case_sensitive = True
        self.recursive = recursive

    def start(self):
        event_handler = PatternMatchingEventHandler(self.patterns,
                                                    self.ignore_patterns,
                                                    self.ignore_directories,
                                                    self.case_sensitive)
        event_handler.on_created = self.__on_created
        event_handler.on_deleted = self.__on_deleted
        event_handler.on_modified = self.__on_modified
        event_handler.on_moved = self.__on_moved

        path = self.dir
        go_recursively = self.recursive

        observer = Observer()
        observer.schedule(event_handler, path, recursive=go_recursively)

        observer.start()
        print(f'Started Watchdog on path {self.dir}')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()

    def __on_created(self, event):
        print(f"{event.src_path} has been created!")

    def __on_deleted(self, event):
        print(f"deleted {event.src_path}!")

    def __on_modified(self, event):
        print(f"{event.src_path} has been modified")

    def __on_moved(self, event):
        print(f"moved {event.src_path} to {event.dest_path}")
