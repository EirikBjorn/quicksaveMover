import shutil, time, json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

steamUserID = "\00000000"
destinationDir = "E:\witcher2"

## Copy save files to another dir
def copySave():
    with open('save.json', 'r+') as f:
        data = json.load(f)
        f.seek(0)
        save = data.get("save")

        print(save)

        saveSrc = r"C:\Program Files (x86)\Steam\userdata" + steamUserID + r"\20920\remote\QuickSave.sav"
        saveDest = destinationDir + "\QuickSave_" + str(save) + ".sav"
        tmbSrc = r"C:\Program Files (x86)\Steam\userdata" + steamUserID + r"\20920\remote\QuickSave_640x360.bmp"
        tmbDest = destinationDir + "\QuickSave_640x360_" + str(save) + ".bmp"  
        newSave = { "save": save + 1 }

        json.dump(newSave ,f)
        f.truncate()
        f.close()

    shutil.copy2(saveSrc, saveDest)
    shutil.copy2(tmbSrc, tmbDest)

## Watch savegame dir for changes
class OnMyWatch:
    dirToWatch = r"C:\Program Files (x86)\Steam\userdata\91034458\20920\remote"

    def __init__(self):
        self.observer = Observer()
  
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.dirToWatch, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
  
        self.observer.join()
  
## Do stuff if there is changes to savegame dir
class Handler(FileSystemEventHandler):
  
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
 
        elif event.event_type == 'created': 
            print("New quicksave has been copied to backup folder")
            copySave()


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()

