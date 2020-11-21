import os
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class ReactoniteWatcher():
    """A file/directory watcher to report events incase
    they are modified/created/deleted.

    Attributes
    ----------
    src_dir : str
        Path of the source direectory to watch and report for events.
    dest_dir : str
        Path of the destination direectory to write transpiled code.
    config_settings : dict
        Path to src_dir and dest_dir as dict object, stored in config.json
    patterns : str, optional
        Pattern of files/directories to watch, defaults to "*"
    ignore_patterns : str, optional
        Pattern of files/directories to ignore or not watch, defaults to ""
    ignore_directories : bool, optional
        Parameter whether the watcher should ignore directories or
        not, defaults to False
    case sensitive : bool
        Parameter explaining whether file/directory names are
        case-sensitive or not, defaults to True
    recursive : bool
        Parameter whether the watcher should recursively watch
        inside directories or not, defaults to True
    """

    def __init__(self,
                 config_settings,
                 patterns="*",
                 ignore_patterns="",
                 ignore_directories=False,
                 case_sensitive=True,
                 recursive=True):

        self.src_dir = config_settings["src_dir"]
        self.dest_dir = config_settings["dest_dir"]
        self.config_settings = config_settings

        if not os.path.exists(os.path.join(".", self.src_dir)):
            raise RuntimeError(
                "Source directory doesn't exist at " +
                str(self.src_dir)
            )

        if not os.path.exists(os.path.join(".", self.dest_dir)):
            raise RuntimeError(
                "Destination directory doesn't exist at " +
                str(self.dest_dir)
            )

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

        go_recursively = self.recursive

        observer = Observer()
        observer.schedule(
            event_handler,
            self.src_dir,
            recursive=go_recursively
        )

        observer.start()

        print(f'Started watching for changes on path {self.src_dir}')
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
