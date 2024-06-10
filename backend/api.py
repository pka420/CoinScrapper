from __future__ import absolute_import, unicode_literals
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import Jobs, Tasks
from backend.serializers import JobCreateSerializer, JobViewSerializer, JobStatusSerializer, TaskSerializer
from rest_framework_tracking.mixins import LoggingMixin
import os
import json
import datetime
from .celery import start_scrapper, finalize_jobs
from celery import chord

hostname = os.getenv("HOSTNAME")
port = os.getenv("PORT")

def create_tasks(data, instance):
    task_list = []
    for coin in instance.coins:
        task = Tasks.objects.create(coin=coin, job=instance)
        task_list.append(task.id)

    task_group = chord(
            (start_scrapper.s(task, hostname, port) for task in task_list),
             )(finalize_jobs.s(task_list))


class JobCreateAPIView(LoggingMixin, CreateAPIView):
    logging_methods = ['POST']
    queryset = Jobs.objects.all()
    serializer_class = JobCreateSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
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
        tasks = Tasks.objects.filter(job=instance)
        if instance.is_completed:
            if instance.success:
                serializer = JobViewSerializer(instance)
                data = serializer.data
                tasks = Tasks.objects.filter(job=instance)
                task_serializer = TaskSerializer(tasks, many=True)
                data['tasks'] = task_serializer.data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Job failed to complete.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Job is not completed yet.'}, status=status.HTTP_200_OK)

