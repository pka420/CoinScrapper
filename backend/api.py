from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import Jobs, Task
from backend.serializers import JobCreateSerializer, JobviewSerializer, JobStatusSerializer, TaskSerializer


def create_tasks(data):
    job_id = data['id']
    coin_list = data['coin_list']
    task_list = []
    for coin in coin_list:
        task = Task.objects.create(coin_name=coin, job_id=job_id)
        task_list.append(task.id)
    job = Jobs.objects.get(id=job_id)
    job.task_list = task_list
    job.save()


class JobCreateAPIView(LoggingMixin, CreateAPIView):
    logging_methods = ['POST']
    queryset = Jobs.objects.all()
    serializer_class = JobCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        serializer = JobCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
                create_tasks(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobViewAPIView(LoggingMixin, RetrieveAPIView):
    logging_methods = ['POST']
    queryset = Jobs.objects.all()
    serializer_class = JobViewSerializer
    lookup_field = 'id'

    get_object(self):
        id = self.kwargs.get('id')
        return Jobs.objects.get(id=id).output_view()



