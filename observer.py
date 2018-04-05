import time
import os
import config
import WorkWithDB
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher(WorkWithDB.ProcessingRequest):

    def __init__(self):
        super().__init__()
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, path=config.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                print('obs')
                if os.path.exists(config.file_path):
                    self.dictation_preprocess()
                    os.remove(config.file_path)
                    print('log file was deleted')
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            f = open('log.txt', 'w')
            f.write('1')
            print('log file was created')



