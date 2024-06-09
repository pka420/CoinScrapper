from django.urls import path

from .api import JobCreateAPIView, JobViewAPIView

urlpatterns = [
    path('taskmanager/start_scraping', JobCreateAPIView.as_view(), name="create-job"),
    path('taskmanager/scraping_status/<uuid:id>', JobViewAPIView().as_view(), name="job-view"),
]
