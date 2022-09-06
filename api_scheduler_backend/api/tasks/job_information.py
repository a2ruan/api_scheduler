from django.db.models import Count
import requests
from ..models import *
from colorama import Fore, init
init(autoreset=True)

def initialize_jobs():
    # Initialize dataset for testing

    # Delete data
    Worker.objects.all().delete()
    APIJob.objects.all().delete()
    APIJobTemplate.objects.all().delete()

    # Create workers
    response = requests.post("http://127.0.0.1:5000/workers", json = {'name':'andy'})
    response = requests.post("http://127.0.0.1:5000/workers", json = {'name':'cindy'})

    # Create job templates
    response = requests.post("http://127.0.0.1:5000/templates", json = {'name':'job1','url':'http://10.6.193.63:5501/send-notification/wombat_server/TEST_MESSAGE1'})
    response = requests.post("http://127.0.0.1:5000/templates", json = {'name':'job2','url':'http://10.6.193.63:5501/send-notification/wombat_server/TEST_MESSAGE2'})
    response = requests.post("http://127.0.0.1:5000/templates", json = {'name':'job3','url':'http://10.6.193.63:5501/send-notification/wombat_server/TEST_MESSAGE2'})

    # Create jobs from each job template, for each worker
    for worker in Worker.objects.all():
        for job in APIJobTemplate.objects.all():
            APIJob.objects.create(name=job.name, url=job.url, worker=worker, apijobtemplate=job)


def execute_tasks():

    print(f"Number of Workers = {Worker.objects.count()}")
    # Iterate through all workers, then iterate through all jobs.
    for worker in Worker.objects.all():
        print(f"\n{Fore.YELLOW}{worker.uuid} {worker.name}")

        # If worker is in stop state or paused state, do not execute
        print(f"Paused = {worker.pause_jobs} Stopped = {worker.stop_jobs}")
        if not worker.pause_jobs and not worker.stop_jobs:
            # Set job to running status if no jobs are currently running
            
            # Removed, uses pause queue method
            #if APIJob.objects.filter(worker=worker, job_type="running").count() == 0:

            # If count is greater than 1, execute one job and set the job to running
            for job in APIJob.objects.filter(worker=worker, job_type="normal").all():

                job.job_type = "running"
                job.save()
                
                # Execute job
                if job.url != None:
                    send_get_request(job.url)
                    
                    # Pause the worker
                    worker.pause_jobs = True
                    worker.save()

                break
            else:
                print("Job already running")
        
        # For each worker, check to see if number of jobs is greater than 0
        print(f">> Number of normal jobs in queue for worker {worker.name}: {APIJob.objects.filter(worker=worker, job_type='normal').count()}")
        print(f">> Number of running jobs for worker {worker.name}: {APIJob.objects.filter(worker=worker, job_type='running').count()}")
        print(f">> Number of debug jobs for worker {worker.name}: {APIJob.objects.filter(worker=worker, job_type='debug').count()}")
        for job in APIJob.objects.filter(worker=worker).all():
            print(f">>>> {job.name} {job.job_type} {job.priority} {job.url}")

def print_jobs():
    print(f"\n\nNumber of Jobs = {APIJob.objects.count()}")
    for job in APIJob.objects.all():
        print(f"{job.name} {job.url}")
    
def send_get_request(url):
    if url is not None and url is not "":
        print(f"Sending request: {url}")
        response = requests.get(url)
        print(response)
    else:
        print("Invalid url")