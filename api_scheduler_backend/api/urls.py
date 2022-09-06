# Recieves requests and routes them to the appropriate 
# This is an application level url routing layer, and routes to the appropriate views.py


from django.urls import path
from .views import *
from .tasks.task_handle import *

# These are routing patterns for REST API
urlpatterns = [
    #path('',main),
    path('workers',WorkerView.as_view()),
    path('workers/uuid/<pk>',WorkerView.as_view()),

    path('jobs',APIJobView.as_view()),
    path('jobs/uuid/<pk>',APIJobView.as_view()),

    path('templates',APIJobTemplateView.as_view()),
    path('templates/uuid/<pk>',APIJobTemplateView.as_view())
]


import uuid
import threading
import time
import sys

thread2 = threading.Thread(target=loop, args=(), daemon=True)
thread2.start()