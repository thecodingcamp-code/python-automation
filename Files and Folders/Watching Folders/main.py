import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

folder = Path("watched")
folder.mkdir(exist_ok=True)

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {Path(event.src_path).name}")

event_handler = NewFileHandler()
observer = Observer()
observer.schedule(event_handler, str(folder), recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()