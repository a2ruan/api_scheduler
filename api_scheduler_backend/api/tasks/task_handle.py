import sys, uuid, time
import threading
from colorama import Fore, init
init(autoreset=True)

from .job_information import *

def loop(): # Main loop that continously runs as a seperate thread (called in urls.py after runserver command).  This thread is destroyed on program exit via a daemon.
    
    # Initialize jobs
    initialize_jobs()

    if "runserver" in sys.argv:
        time.sleep(5)
        uuid_r = uuid.uuid4
        while True:
            print(f"\n{Fore.GREEN}-- Starting Poll -- ")
            task_executor = threading.Thread(target = execute_tasks, args=(), daemon=True)
            task_executor.start()

            time.sleep(10)
            print(f"{Fore.YELLOW}-- Ending Poll -- ")

#### Custom Tasks ####





