#from django.test import TestCase

# Create your tests here.
import requests, time
import urllib.request

# Testing post new worker

def post_new_worker(name="Random"):
    response = requests.post("http://127.0.0.1:5000/workers", json = {'name':name})
    #print(response)
    return response.content.decode("utf-8") or None

def delete_worker(name="Random"):
    for list_item in eval(get_worker()):
        uuid = list_item['uuid']
        if list_item['name'] == name:
            # Note: only the delete function will delete the row
            requests.delete(f"http://127.0.0.1:5000/workers/uuid/{uuid}")
            
    return None

def modify_worker(name="Random", new_val_dict={}):
    # Modify worker given inputs
    for list_item in eval(get_worker()):
        uuid = list_item['uuid']
        if list_item['name'] == name:
            r = requests.patch(f"http://127.0.0.1:5000/workers/uuid/{uuid}", data = new_val_dict)
            print(r.content)


def get_worker():
    response = requests.get("http://127.0.0.1:5000/workers")
    #print(response.content)
    return response.content.decode('utf-8') or None

def get_worker2():
    response = urllib.request.urlopen('http://127.0.0.1:5000/workers')
    html = response.read()



if __name__ == "__main__":
    
    
    # Post, Get
    for i in range(5):
        start_time = time.time()
        post_new_worker(str(time.time()))        
        print(f"Total elapsed time: {time.time() - start_time}")
    print("Finished creating workers")
    time.sleep(5)


    # Patch
    for list_item in eval(get_worker()):
        start_time = time.time()
        uuid = list_item['uuid']
        old_name = list_item['name']
        new_name = "worker_" + str(old_name)

        payload = {
            'name':new_name
        }

        modify_worker(old_name, payload)
        print(f"Total elapsed time: {time.time() - start_time}")
    
    print("Finished patching workers")
    time.sleep(10)


    # Delete
    for list_item in eval(get_worker()):
        start_time = time.time()
        uuid = list_item['uuid']
        name = list_item['name']
        delete_worker(name)
        print(f"Total elapsed time: {time.time() - start_time}")
    
    print("Finished deleting workers")