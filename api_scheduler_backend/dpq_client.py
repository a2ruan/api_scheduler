from redis_priority_queue import redis_priority_queue
from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
import psutil, time, requests, os
import json

SERVER_IP = "localhost"
SERVER_PORT = 5000
SLEEP_TIME = 10
app = FastAPI()

# Server Side Functional Calls

# Utilities
@app.get("/scheduler_status")
def process_status(executable_name:str="python", file_name=["scheduler.py"], request:Request=None) -> bool:
    """Determines if python program scheduler is running or not on the current computer

    Args:
        executable_name (str, optional): Name of the executable to search for. Defaults to "python".
        file_name (str, optional): The file name of the file being run. Defaults to "scheduler-script.py".
        request (Request, optional): Defaults to None.

    Returns:
        bool: True if the program is running on the current computer, otherwise False
    """
    for proc in psutil.process_iter():
        try:
            if executable_name in proc.name():
                print("--")
                print(proc.cmdline())
                print(proc.name())
                process_executable_name = proc.cmdline()
                for token in process_executable_name:
                    print(token)
                    print("Comparing to:")
                    print(file_name)
                    for file in file_name:
                        if file in token:
                            print(f"Found {file_name} in {process_executable_name}")
                            return True
        except Exception as e:
            print(e)
    return False

@app.get("/cleanup")
def cleanup(request:Request=None) -> bool:
    try:
        print("Cleanup roaming")
        roaming_folder = os.path.join(os.environ.get("APPDATA"))
        files_to_delete = os.listdir(roaming_folder)
        print(files_to_delete)
        for files in files_to_delete:
            full_file_path = os.path.join(roaming_folder,files)
            if os.path.isfile(full_file_path):
                print(f"File found at {full_file_path}. Attempting to delete")
                try:
                    os.remove(full_file_path)
                except Exception as e1:
                    print(f"Unable to delete file due to {e1}")
        return True
    except Exception as e:
        print(e)
        return False

@app.get("/labels")
def get_labels(request:Request=None) -> list:
    """Get a list of labels for determining which queue to pull from first.  List is ordered based on precendence.

    Args:
        request (Request, optional): Request information for post REST requests. Defaults to None.

    Returns:
        list: Returns an ordered list of labels
    """
    labels = []
    scheduler_labels = os.environ.get("SCHEDULER_LABELS",None)
    print(scheduler_labels)
    if scheduler_labels != None: labels.extend(scheduler_labels.split(","))
    scheduler_labels = os.environ.get("JENKINS_LABEL",None)
    if scheduler_labels != None: labels.append(scheduler_labels)
    
    # Also add additional motherboard information: motherboard_type, manufacturer, vbios uuid, vbios name, boardid, asic family, global keyword
    # Pending for later when global queues are enabled
    return labels 

#@app.on_event("startup")
@app.get("/add_dummy_data")
def dummy_data(request:Request=None):
    print("Dummy Data Injection into Redis Queues")
    labels = get_labels()
    if len(labels) > 0:
        output = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/populate2/?name={labels[0]}")
        print(output.text)    

@app.on_event("startup")
@app.get("/next")
@repeat_every(seconds=5)
def next(request:Request=None) -> dict:
    if process_status("python",["scheduler-script.py","scheduler.py"]):
        print(f"Scheduler is currently running.  Sleeping for {str(SLEEP_TIME)}s.")
        time.sleep(SLEEP_TIME)
    else:
        # Iterate through all labels and run next job in queue
        labels = get_labels()
        output_dict = {}
        print("Polling for all queues")
        print(labels)
        for label in labels:
            output = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/pop/?name={label}")
            output_dict = output.json()
            if output_dict != {}: 
                print(f"Found a job in queueName={label}")
                print(output.json())
                break
        
        if output_dict == {}:
            print(f"No job in queue. Sleeping for {str(SLEEP_TIME)}s.")
            time.sleep(SLEEP_TIME)
        else:
            print("Scheduling next job.")
            
            cleanup()
            time.sleep(1)
            
            print("Writing dictionary to JSON")
            test_dict = output_dict["value"]
            for test_case in test_dict:
                if "TP::skip" in test_dict[test_case]:
                    test_dict[test_case]["TP::skip"] = "no"
            file_name = output_dict["uuid"]
            with open(f"C:/Storage/current_job.json","w") as f:
                json.dump(test_dict, f, indent=4)
                
            if os.path.exists("C:/Storage/current_job.json"):
                print("Calling on scheduler")
                import uuid
                command = "start cmd.exe -title 'redis_scheduler_" + str(uuid.uuid4()) + "' /c scheduler C:/Storage/current_job.json"
                print(command)
                os.system(command)
                print("Done command")
                time.sleep(10)
            else:
                print("No JSON exists")
            
    return {}

def kill_process_except(program_name, process_name):
    # Given a program name i.e cmd.exe and process name i.e internet, the function will kill
    # all associated cmd.exe programs except those containing the process name as a substring.  
    
    process_to_kill = program_name
    my_pid = os.getpid()

    # Iterate through all processes, and kill processes  matching the program_name and not contains process_name within its name
    for p in psutil.process_iter():
        if p.name() == process_to_kill:
            list_of_paths = p.cmdline().copy()
            for item_name in list_of_paths:
                print(p.name() + "--" + item_name)
                if process_name.lower() not in item_name.lower(): # Note: disallow function from closing itself?
                    print("Killing process PID=" + str(p.pid) + "-" + str(process_name))        
                    p.kill()
                    break

if __name__ == "__main__":
    print("Initializing Scheduler Client")
    
    # The process to determine if program is running is to use psutil to poll for python.exe and its script name
    # While program is running, scheduler-script.py must be running.  Therefore, if any instance of scheduler-script.py is present, program is still running.
    
    # Once the computer is idle for longer than a set duration, this client will call on the scheduler engine for the next job in queue.
    # If no job is in queue, the client will sleep for a longer duration to avoid overloading the load balancer / server.
    
    while True:
        
        if process_status("python",["scheduler.py","scheduler-script.py"]):
            time.sleep(60)
        else:
            # Run next job in queue
            output = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/pop/?name=RACK_A2")
            output_dict = output.json()
            if output_dict == {}: 
                print("Sleeping for long time")
                time.sleep(60)
            print(output.json())
            
        time.sleep(0.1)
            