
# Hello world
from django.shortcuts import render
from django.http import HttpResponse

# Serializers 
from .models import *
from rest_framework import generics
from .serializers import RoomSerializer, WorkerSerializer

# React connection
from rest_framework.response import Response

# Create your views here.
# Views are functions that return an output i.e JSON

import time

def main(request):
    return HttpResponse("Hello")

class WorkerView(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    


class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request):
        #output = {'hello':'world'}
        output = {'hello':f'world current time = {time.time()}'}
        return Response(output)
    