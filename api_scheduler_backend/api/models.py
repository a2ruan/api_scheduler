# Data models and entitites and relationships between data

from django.db import models
from django.utils.timezone import now # For populating datetime fields
#from django.db.models import JSONField
import string
import random
import uuid

# def generate_unique_code():
#     # Generate unique code for room
#     length = 6
#     while True:
#         code = ''.join(random.choices(string.ascii_uppercase),k=length)
#         if Room.objects.filter(code=code).count() == 0:
#             # Only exit if code is unique for all room objects
#             break
#     return code

class Worker(models.Model):
    # A worker represents a computer/device.  Each worker has an independant job queue (for normal jobs and debug jobs)
    # For grouping workers together by location or identifier
    group = models.TextField(default="bkc_regression")

    # Fields for self identification
    uuid = models.UUIDField(primary_key=True, default = uuid.uuid4)
    name = models.TextField(default="", unique=True)
    date_created = models.DateTimeField(default=now)

    # Worker Options
    auto_debug = models.BooleanField(default=False) # Indicates whether the worker will auto-trigger the debug queue on system hang
    pause_jobs = models.BooleanField(default=False) # Indicates whether the worker's queued jobs are currently paused.  This does not stop the debug queue if the timeout is reached
    stop_jobs = models.BooleanField(default=False) # Allows users to stop the worker from executing, including the debug queue
    saved_job_limit = models.IntegerField(default=20) # Max number of previous jobs that have run, that will be saved
    timeout_limit = models.IntegerField(default=300) # Amount of time (s) that a worker can be paused before triggering debug queue
    max_debug_attempts = models.IntegerField(default=1) # Max number of times debug can be triggered before full stop
    current_debug_attempts = models.IntegerField(default=0) # Current number of times worker tried debug queue
    kwargs = models.TextField(default="") # Default args attached to worker

    # Worker State
    last_active_time = models.DateTimeField(default=now)
    last_active_debug_time = models.DateTimeField(default=now)

class APIJobTemplate(models.Model):
    # A job template is a reusable generic job for sending a REST API call.
    guid = models.UUIDField(default = uuid.uuid4) # Jobs are linked by guid
    url = models.TextField(default="") # Rest API call url
    name = models.TextField(default="")

    # There are two api options: get, post
    api_method = models.TextField(default="get")

    #class Meta:
    #    abstract = True

class APIJob(models.Model):
    # A Job represents an action to be performed.  For this project, it is sending a REST API call.  
    # The Job table stores the following:
    # 1) PendingJobs - jobs that are scheduled to run in the future
    # 2) CurrentJobs - jobs that are currently running
    # 3) PreviousJobs - jobs that have previously run in the past.  This category can be moved to seperate Table for improved speed.

    uuid = models.UUIDField(primary_key=True, default = uuid.uuid4)
    priority = models.IntegerField(default=0)

    # There are two types of job_types:
    # 1) normal - normal jobs are for typical scheduling
    # 2) debug - debug jobs are jobs that are run if a Worker becomes unresponsive.  
    # Debug jobs are typically used for recovery of the worker node i.e rebooting worker remotely
    job_type = models.TextField(default="normal")

    # Job options
    iterations = models.IntegerField(default=1) # Number of iterations to repeat this job
    max_retries = models.IntegerField(default=3) # Max retries before job turns into low priority
    retry_count = models.IntegerField(default=0) # Current number of retries
    kwargs = models.TextField(default="") # Default args attached to job
    
    # Foreign key linking the job to a Worker
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE) # Link a job to a worker.  The job will get deleted if the worker is deleted (cascade)
    apijobtemplate = models.ForeignKey(APIJobTemplate, on_delete=models.CASCADE) # Link a job template to a job.  The job will get deleted if the api job template is deleted (cascade)


# Create your models here.
class Room(models.Model):
    code = models.CharField(max_length=8, default="", unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    