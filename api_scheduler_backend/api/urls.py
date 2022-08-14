from django.urls import path
from .views import *

# These are routing patterns for REST API
urlpatterns = [
    #path('',main),
    path('room-create',RoomView.as_view()),
    path('room-list',RoomList.as_view()),
    path('room-view',RoomView.as_view())
]