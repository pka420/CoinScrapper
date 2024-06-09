from __future__ import absolute_import, unicode_literals
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import Jobs, Tasks
from backend.serializers import JobCreateSerializer, JobViewSerializer, JobStatusSerializer, TaskSerializer
from rest_framework_tracking.mixins import LoggingMixin
import os
from celery import Celery
import json
import datetime
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_celery.settings")
app = Celery('coin_scrapper')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

hostname = os.getenv("HOSTNAME")
port = os.getenv("PORT")

@app.task(bind=True)
def start_task(self, task_id):
    cmd = f"python main.py -n {hostname} -p {port} -i {task_id}"
    subprocess.run(cmd, shell=True)

def create_tasks(data, instance):
    for coin in instance.coins:
        task = Tasks.objects.create(coin=coin, job=instance)
        start_task.apply_async(args=[task.id])


class JobCreateAPIView(LoggingMixin, CreateAPIView):
    logging_methods = ['POST']
    queryset = Jobs.objects.all()
    serializer_class = JobCreateSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        for each in data['coins']:
            print(each)
        data['submitted_on'] = datetime.datetime.now()

        serializer = JobCreateSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            create_tasks(serializer.data, instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobViewAPIView(LoggingMixin, RetrieveAPIView):
    logging_methods = ['POST']
    queryset = Jobs.objects.all()
    serializer_class = JobViewSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_completed:
            print('Job is completed')
            serializer = JobViewSerializer(instance)
            data = serializer.data

            tasks = Tasks.objects.filter(job=instance)
            task_serializer = TaskSerializer(tasks, many=True)

            return Response(data, status=status.HTTP_200_OK)
        else:
            print('Job is not completed')
            return Response({'message': 'Job is not completed'}, status=status.HTTP_200_OK)

