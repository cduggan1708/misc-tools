import sys, getopt
from datetime import datetime, timedelta, date
import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
import shutil

# need to install watchdog and shutilwhich

PROJECT_HOME = "C:\\Users\\cduggan\\workspace\\"
XAMPP_HOME = "C:\\xampp\\htdocs\\"

class DirectoryHandler(PatternMatchingEventHandler):
    updateDirectory = ""
    patterns = ["*.php", "*.css", "*.map", ".ini"]

    def setUpdateDirectory(self, updateDirectory):
        self.updateDirectory = updateDirectory

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print(event.src_path, event.event_type)  # print now only for debug

        # handle subdirectories by getting the file path after splicing PROJECT_HOME
        filepath = event.src_path[len(PROJECT_HOME):]
        file_parts = filepath.split("\\")
        toDirectory = self.updateDirectory
        if len(file_parts) > 2: # root directory and filename expected (2)
            for i in range(1, len(file_parts)): #  skip root directory
                toDirectory += "\\" + file_parts[i]

	    # copy to xampp directory
        shutil.copy2(event.src_path, toDirectory)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def handleWatching(projectDirectory, xamppDirectory):
    observer = Observer()
    dh = DirectoryHandler()
    dh.setUpdateDirectory(xamppDirectory)
    observer.schedule(dh, path=projectDirectory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def main(argv):
    projectDirectory = ""
    xamppDirectory = ""
    
    try:
        opts, args = getopt.getopt(argv, "hp:x:")
    except:
        print('update_xampp_files.py -p <project directory> -x <XAMPP directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('update_xampp_files.py -p <project directory> -x <XAMPP directory>')
            sys.exit()
        else:
            if opt in ('-p', '--projectDirectory'):
                projectDirectory = PROJECT_HOME + arg
            if opt in ('-x', '--xamppDirectory'):
                xamppDirectory = XAMPP_HOME + arg

    if projectDirectory != "" and xamppDirectory != "":
        print("%s: Executed update_xampp_files.py" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("When updates to %s are made, %s will automatically be updated" % (projectDirectory, xamppDirectory))
        handleWatching(projectDirectory, xamppDirectory)
    

if __name__ == '__main__':
    main(sys.argv[1:])
