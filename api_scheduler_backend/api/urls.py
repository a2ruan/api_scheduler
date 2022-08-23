# Recieves requests and routes them to the appropriate 
# This is an application level url routing layer, and routes to the appropriate views.py


from django.urls import path
from .views import *

# These are routing patterns for REST API
urlpatterns = [
    #path('',main),
    path('room-create',RoomView.as_view()),
    path('room-list',RoomList.as_view()),
    path('room-view',RoomView.as_view()),
    path('workers',WorkerView.as_view()),
    path('workers/uuid/<pk>',WorkerView.as_view()),
]