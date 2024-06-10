from django.db import models

# Create your models here.

from django_bleach.models import BleachField
import json
import os
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import JSONField


class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey('Jobs', on_delete=models.CASCADE, related_name='task_list', null=False)
    coin = models.CharField(max_length=20)
    ip_address = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    price_change = models.CharField(max_length=20, blank=True, null=True)
    market_cap = models.CharField(max_length=20, blank=True, null=True)
    market_cap_rank = models.CharField(max_length=20, blank=True, null=True)
    volume = models.CharField(max_length=20, blank=True, null=True)
    volume_rank = models.CharField(max_length=20, blank=True, null=True)
    volume_change = models.CharField(max_length=20, blank=True, null=True)
    circulating_supply = models.CharField(max_length=20, blank=True, null=True)
    total_supply = models.CharField(max_length=20, blank=True, null=True)
    diluted_market_cap = models.CharField(max_length=20, blank=True, null=True)
    contracts = JSONField(default=list, blank=True, null=True)
    official_links = JSONField(default=list, blank=True, null=True)
    social = JSONField(default=list, blank=True, null=True)
    is_running = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    selenium_logs = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coin_name

    def output_view(self):
        return json.dumps({
                           'coin': self.coin_name,
                           'output': json.dumps({
                               'price': self.price,
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


class Jobs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coins = ArrayField(models.CharField(max_length=20), default=list, size=8)
    is_completed = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    submitted_on = models.DateTimeField(auto_now=False, default=timezone.now, null=True, blank=True)
    finished_on = models.DateTimeField(auto_now=False, default=timezone.now, null=True, blank=True)

    def output_view(self):
        return json.dumps({
            'job_id': self.id,
            'tasks': json.dumps([task.output_view for task in self.task_list])
        })



