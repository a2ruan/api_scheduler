# Convert python objects and structures into JSON for consumption by front-end

from rest_framework import serializers
from .models import *

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