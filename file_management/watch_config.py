import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from serv_logging.serv_logging import Logging

class WatchdogConfig:
    STOP_LOOP = False

    def __init__(self, call_back, path, file_pattern, ignore_pattern, ignore_dirs, recursive, case_sensitive, log_path):
        self.__logger = Logging.getInstance(Logging.DEB)
        self.__logger.open(log_path)

        self.__call_back = call_back

        self.__logger.write(Logging.INF, "Creating monitor of file path: " + path + ", with pattern: " + file_pattern + ", ignoring: " + ignore_pattern + ", dir ignore? " + str(ignore_dirs) + ", recursive? " + str(recursive) + ", case sensitivity? " + str(case_sensitive) + ", with callback: " + self.__call_back.__name__)

        self.__watchdog_handler = PatternMatchingEventHandler(file_pattern, ignore_pattern, ignore_dirs, case_sensitive)
        self.__watchdog_handler.on_created = self.on_created
        self.__watchdog_handler.on_modified = self.on_modified

        self.__watchdog_observer = Observer()
        self.__watchdog_observer.schedule(self.__watchdog_handler, path, recursive=recursive)

    def on_created(self, event):
        self.__logger.write(Logging.INF, "Created: " + event.src_path)
        self.__call_back()

    def on_modified(self, event):
        self.__logger.write(Logging.INF, "Modified: " + event.src_path)
        self.__call_back()

    def start_observing(self):
        self.__watchdog_observer.start()
        try:
            while not WatchdogConfig.STOP_LOOP:
                time.sleep(1)
        except (Exception, KeyboardInterrupt) as e:
            #self.__watchdog_observer.stop()
            #self.__watchdog_observer.join()
            self.__logger.write(Logging.WAR, "Stopped observing config: " + str(e))
        finally:
            self.__watchdog_observer.stop()
            self.__watchdog_observer.join()
            self.__logger.write(Logging.WAR, "Stopped observing config gracefully")