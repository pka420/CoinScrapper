import base64
import os
from fileinput import filename

from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog

from backend.models import Jobs, Task


class JobCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    class Meta:
        model = Jobs
        fields = '__all__'

class JobViewSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Jobs
        fields = '__all__'


class JobStatusSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Jobs
        fields = [ 'id', 'is_running', 'is_completed']

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Task
        fields = '__all__'
