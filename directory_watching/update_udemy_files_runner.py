import subprocess
import sys
import inspect
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def get_script_dir(follow_symlinks=True):
    # from http://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory-in-python/22881871#22881871
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def kick_off_script():
    script_dir = get_script_dir()
    subprocess.call([sys.executable, os.path.join(get_script_dir(), 'update_xampp_files.py'), '-p', 'udemy', '-x', 'udemy'])
    
def main():
    kick_off_script()

if __name__ == '__main__':
    main()