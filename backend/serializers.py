import base64
import os
from fileinput import filename

from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog

from backend.models import Jobs, Tasks


class JobCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    class Meta:
        model = Jobs
        exclude = ['finished_on']


class JobViewSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Jobs
        exclude = ['coins', 'is_running', 'is_completed']


class JobStatusSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Jobs
        fields = [ 'id', 'is_running', 'is_completed']

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Tasks
        exclude = ['job', 'selenium_logs']


class TaskUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Tasks
        fields = ['__all__']
