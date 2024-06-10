from celery import Celery
import os
from datetime import datetime
import pytz


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapper.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=False,ignore_result=True)
def start_scrapper(task_id, hostname, port):
    from .scrapper import Scrapper
    scrap = Scrapper(task_id, hostname, port)
    scrap.run_scrapper()

@app.task(bind=False,ignore_result=True)
def finalize_jobs(results, task_list):
    from .models import Jobs
    from .models import Tasks

    job = Jobs.objects.get(task_list=task_list[0])
    timezone = pytz.timezone('Asia/Kolkata')

    job.is_completed = True
    job.finished_on = datetime.now(timezone)
    job.save()

    if all(task.is_completed for task in Tasks.objects.filter(id__in=task_list)):
        job.success = True
        job.save()
        return True

    return False
