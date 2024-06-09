from django.db import models

# Create your models here.

from django_bleach.models import BleachField
import json
import os
import uuid

from account.models import User
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coin_name = models.CharField(max_length=200)
    price = models.CharField(max_lenght=20)
    price_change = models.CharField(max_lenght=20)
    market_cap = models.CharField(max_lenght=20)
    market_cap_rank = models.CharField(max_lenght=20)
    volume = models.CharField(max_lenght=20)
    volume_rank = models.CharField(max_length=20)
    volume_change = models.CharField(max_lenght=20)
    circulating_supply = models.CharField(max_lenght=20)
    total_supply = models.CharField(max_lenght=20)
    diluted_market_cap = models.CharField(max_lenght=20)
    contracts = ArrayField(models.CharField(max_length=200), default=list)
    official_links = ArrayField(models.CharField(max_length=200), default=list)
    social = ArrayField(models.CharField(max_length=200), default=list)
    is_running = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    selenium_logs = models.CharField(max_length=200)

    def __str__(self):
        return self.coin_name

    def output_view(self):
        return json.dumps({
                           'coin': self.coin_name,
                           'output': json.dumps({
                               'price': self.price
                               'price_change': self.price_change,
                               'market_cap': self.market_cap,
                               'market_cap_rank': self.market_cap_rank,
                               'volume': self.volume,
                               'volume_rank': self.volume_rank,
                               'volume_change': self.volume_change,
                               'circulating_supply': self.circulating_supply,
                               'total_supply': self.total_supply,
                               'diluted_market_cap': self.diluted_market_cap,
                               'contracts': self.contracts,
                               'official_links': self.official_links,
                               'social': self.social
                           })
                        })
    def logs_view(self):
        return json.dumps({
            'coin': self.coin_name,
            'logs': self.selenium_logs
        })


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_list = models.ManyToManyField(Task)
    coin_list = ArrayField(models.CharField(max_length=20), default=list, size=8)
    ip_address = models.CharField(max_length=200)
    is_running = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def output_view(self):
        return json.dumps({
            'job_id': self.id,
            'tasks': json.dumps([task.output_view for task in self.task_list])
        })



