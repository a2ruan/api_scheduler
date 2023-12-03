from redis_priority_queue import redis_priority_queue
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import json
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
import os
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


redis_queue_manager = redis_priority_queue(ip="10.1.100.100", port=7000, mode="cluster")

templates = Jinja2Templates(directory="..")

@app.get("/queue-dict/{queue_name}")
def get_queue_dict(queue_name:str=None, request:Request=None):
    #print(queue_name)
    kwargs = {}
    
    queued_jobs = get(queue_name)
    #print(queued_jobs)
    jobs = []
    for job in queued_jobs:
        #print(job)
        #print(job.get("uuid"))
        #print(job.get("value"))
        jobs.append({'id':str(job.get("uuid")).replace("-",""),"name":str(list(job.get("value").keys())[0]), "json":job.get("value"),"score":job.get("score")})
    return jobs

@app.get("/queue/{queue_name}")
def main_webpage(queue_name:str=None, request:Request=None):
    #print(queue_name)
    kwargs = {}

    queued_jobs = get(queue_name)

    kwargs["queue_name"] = queue_name
    kwargs["queued_jobs"] = queued_jobs
    return templates.TemplateResponse("dynamic_scheduler/templates/main.html", {"request":request,"kwargs":kwargs})

@app.get("/edit")
def clear(name:str,id:str,obj:object,request:Request=None):
    print("Editing")
    return redis_queue_manager.edit(name,obj,id)

# Abstract Interface to Redis Queue Manager

@app.get("/clear")
def clear(name:str,request:Request=None):
    redis_queue_manager.clear(name)

@app.get("/set_priority")
def set_priority(name:str=None, index:int=None, score:float=None, request:Request=None):
    redis_queue_manager.set_priority(name ,index, score)

@app.get("/rem")
def rem(name:str, index:int,request:Request=None):
    redis_queue_manager.rem(name, index)

@app.get("/swap")
def swap(name:str=None, source_index:int=None, target_index:int=None,request:Request=None):
    redis_queue_manager.swap(name, source_index, target_index)

@app.get("/drag")
def swap(name:str=None, source_index:int=None, target_index:int=None,request:Request=None):
    redis_queue_manager.drag(name, source_index, target_index)

@app.get("/add")
def add(name:str=None, data:dict=None, request:Request=None):
    name = request.headers.get("name",None)
    data = request.headers.get("data",None)
    if name == None: name = dict(request.query_params).get("name","default")
    if data == None: data = json.loads(dict(request.query_params).get("data",'{}')) or {}
    redis_queue_manager.add(name, data)
    return {name:data}

@app.get("/get")
def get(name:str=None, request:Request=None):
    return redis_queue_manager.get(name)

@app.get("/queue_names")
def get_queues(match:str=None, request:Request=None):
    return redis_queue_manager.get_queue_names(match=match)

@app.get("/queues")
def get_queues(match:str=None, request:Request=None):
    return redis_queue_manager.get_queues(match=match)

@app.get("/pop")
def pop_min(name:str=None, request:Request=None):
    return redis_queue_manager.pop_min(name)

@app.get("/populate2")
def populate(name:str=None, request:Request=None):

    dummy_test = {
        "usb_data_transfer_no_acpi_no_amf":{
            "TP::skip":"yes",
            "TP::namespace":"usb"
        }
    }

    for i in range(2):
        redis_queue_manager.add(name,dummy_test)

@app.get("/add_test_plan")
def add_test_plan(name:str=None, json_name:str=None, json_path:str=None, request:Request=None):
    print("Adding Test Plan")
    root_path = r"C:\tests"
    file_list = {}
    for root, dirs, files in os.walk(root_path, topdown=False):
        for fname in files:
            full_path = os.path.join(root, fname)
            if ".json" in full_path:
                #print(full_path)
                file_list[os.path.join(root, fname)] = fname
    
    target_file = None
    for file in file_list:
        #print(file)
        if json_path != None:
            normalized_json_path = json_path.replace("\\","")
            normalized_file = file.replace("\\","")
    
            #print(f"comparing {normalized_file} {type(normalized_file)}")
            #print(f"with {normalized_json_path} {type(normalized_json_path)}")
            if str(normalized_json_path).replace("\"","") in str(normalized_file).replace("\"",""):
                print("Found!")
                target_file = file
                break
        elif json_name != None:
            if json_name.lower() == file_list[file].replace(".json","").lower():
                print("Found!")
                target_file = file
                break
    
    if target_file != None:
        # Convert to dictionary

        # Iterate through all test cases

        # Add to plan, with TP skip disabled for all
        data = {}
        with open(target_file) as json_file:
            data = json.load(json_file)

        for test in data:
            try:
                print("ADDING")
                payload={test:data[test]}
                print({test:data[test]})
                print(name)
                
                result = redis_queue_manager.add(name,payload)
                print("Result=")
                print(result)
            except Exception as e:
                print("ERROR!!")
                print(e)
        return data
    else:
        print("Not found!!!"*100)
    return file_list


@app.get("/get_test_plan_paths")
def get_test_plan_paths(name:str=None, json_name:str=None, request:Request=None):

    root_paths = [r"C:\tests",r"C:\test_plans"]
    
    file_list = []
    for superpath in root_paths:
        for root, dirs, files in os.walk(superpath, topdown=False):
            for fname in files:
                full_path = os.path.join(root, fname)
                if ".json" in full_path:
                    print(full_path)
                    file_list.append({"label":full_path.replace(superpath,""),"path":full_path,"name":fname})
    return file_list

@app.get("/populate")
def populate(request:Request=None):
    test_instances = 5
    racks = 5
    for i in range(test_instances):
        print(f"Adding {i}")
        for i in range(racks):
            redis_queue_manager.add(f"RACK_A{str(i)}",{"hello_world":f"A{i}","type":f"rack{i}","integers":[1,2,3,4]})

# Utility Functions

def decrypt_header(variable_names=[],request:Request=None):
    decrypted_header = {}
    for variable_name in variable_names:
        print(variable_name)
        tentative_value1 = request.headers.get(variable_name,None)
        #tentative_value2 = dict(request.query_params).get(variable_name,None)  # No need for this, it is already in FastAPI by default
        if tentative_value1 != None: decrypted_header[variable_name] = tentative_value1
        #elif tentative_value2 != None: decrypted_header[variable_name] = tentative_value2 # No need for this, it is already in FastAPI by default
    return decrypted_header