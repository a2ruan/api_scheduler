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
            requests.delete(f"http://127.0.0.1:5000/workers/{uuid}")
            
    return None

def get_worker():
    response = requests.get("http://127.0.0.1:5000/workers")
    #print(response.content)
    return response.content.decode('utf-8') or None

def get_worker2():
    response = urllib.request.urlopen('http://127.0.0.1:5000/workers')
    html = response.read()



if __name__ == "__main__":
    
    
    # Post, Get
    for i in range(100):
        start_time = time.time()
        #post_new_worker(str(time.time()))
        #get_worker()
        #get_worker2()
        
        #print(f"Total elapsed time: {time.time() - start_time}")

    # Delete
    delete_worker('cindy ruan')

    
            