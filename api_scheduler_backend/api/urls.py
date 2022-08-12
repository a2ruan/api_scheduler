from django.urls import path
from .views import main
from .views import RoomView
from .views import RoomList

urlpatterns = [
    path('',main),
    path('room-create',RoomView.as_view()),
    path('room-list',RoomList.as_view()),
    path('room-view',RoomView.as_view())
]