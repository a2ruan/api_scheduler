# Handle requests and return responses
# This is the primary REST API routing layer for handling CRUD requests


# Hello world
from django.shortcuts import render
from django.http import HttpResponse

# Serializers 
from .models import *
from rest_framework import generics
from .serializers import * #RoomSerializer, WorkerSerializer

# React connection
from rest_framework.response import Response

# Create your views here.
# Views are functions that return an output i.e JSON

import time

def main(request):
    return HttpResponse("Hello")

#class WorkerView(generics.ListCreateAPIView, generics.DestroyAPIView):
class WorkerView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class APIJobTemplateView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = APIJobTemplate.objects.all()
    serializer_class = APIJobTemplateSerializer

class APIJobView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = APIJob.objects.all()
    serializer_class = APIJobSerializer
