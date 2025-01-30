import os
import shutil
import time
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

source_dir = "C:/Users/gianl/Downloads"
dest_dir_sfx = "C:/Users/gianl/OneDrive/Desktop/Sound"
dest_dir_music = "C:/Users/gianl/OneDrive/Desktop/Music"
dest_dir_videos = "C:/Users/gianl/OneDrive/Desktop/Videos"
dest_dir_images = "C:/Users/gianl/OneDrive/Desktop/Images"


def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move(dest, entry, name):
    file_exists = os.path.exists(f"{dest}/{name}")
    if file_exists:
        unique_name = make_unique(dest, name)
        shutil.move(entry, f"{dest}/{unique_name}")
    else:
        shutil.move(entry, dest)


class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                if name.endswith((".wav", ".mp3")):
                    dest = (
                        dest_dir_sfx
                        if entry.stat().st_size < 25000000 or "SFX" in name
                        else dest_dir_music
                    )
                elif name.endswith((".mov", ".mp4")):
                    dest = dest_dir_videos
                elif name.endswith((".jpg", ".jpeg", ".png")):
                    dest = dest_dir_images
                else:
                    continue
                move(dest, entry, name)


def main():
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
