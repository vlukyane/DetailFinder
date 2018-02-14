import time
import os
import WorkWithDB
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher(WorkWithDB.ProcessingRequest):
    DIRECTORY_TO_WATCH = "/home/vukyane/Pytin/bot/filefoldr"

    def __init__(self):
        super().__init__()
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, path=self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                print('obs')
                file_path = '/home/vukyane/Pytin/bot/log.txt'
                if os.path.exists(file_path):
                    self.dictation_preprocess()
                    os.remove(file_path)
                    print('log file has been deleted')
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
            print('log file has been created')



