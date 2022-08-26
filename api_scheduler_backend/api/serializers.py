# Convert python objects and structures into JSON for consumption by front-end

from rest_framework import serializers
from .models import *

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id','code','host','guest_can_pause','votes_to_skip', 'created_at')

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__' # Expose all fields

class APIJobTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIJobTemplate
        fields = '__all__' # Expose all fields

class APIJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIJob
        fields = '__all__' # Expose all fields