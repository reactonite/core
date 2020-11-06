import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class ReactoniteWatcher():
    """A file/directory watcher to report events incase
    they are modified/created/deleted.

    Attributes
    ----------
    dir : str
        Path of the directory to watch and report for events.
    patterns : str, optional
        Default value = "*"
        Pattern of files/directories to watch
    ignore_patterns : str, optional
        Default value = ""
        Pattern of files/directories to ignore or not watch
    ignore_directories : bool, optional
        Default value = False
        Parameter whether the watcher should ignore directories or
        not
    case sensitive : bool
        Default value = True
        Parameter explaining whether file/directory names are
        case-sensitive or not
    recursive : bool
        Default value = True
        Parameter whether the watcher should recursively watch
        inside directories or not
    """
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
        """Runs the watchdog service on the given path. Handles
        various events to different functions as per the
        requirement
        """
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
        """This event is called when a file/directory
        is created.

        Parameters
        ----------
        event : obj
            An event object containing necessary details about it.
        """
        print(f"{event.src_path} has been created!")

    def __on_deleted(self, event):
        """This event is called when a file/directory
        is deleted.

        Parameters
        ----------
        event : obj
            An event object containing necessary details about it.
        """
        print(f"deleted {event.src_path}!")

    def __on_modified(self, event):
        """This event is called when a file/directory
        is modified.

        Parameters
        ----------
        event : obj
            An event object containing necessary details about it.
        """
        print(f"{event.src_path} has been modified")

    def __on_moved(self, event):
        """This event is called when a file/directory
        is moved.

        Parameters
        ----------
        event : obj
            An event object containing necessary details about it.
        """
        print(f"moved {event.src_path} to {event.dest_path}")
