# Generated by Django 5.0.6 on 2024-06-09 19:23

import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coins', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=8)),
                ('is_running', models.BooleanField(default=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('submitted_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('finished_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coin', models.CharField(max_length=20)),
                ('ip_address', models.CharField(blank=True, max_length=20, null=True)),
                ('price', models.CharField(blank=True, max_length=20, null=True)),
                ('price_change', models.CharField(blank=True, max_length=20, null=True)),
                ('market_cap', models.CharField(blank=True, max_length=20, null=True)),
                ('market_cap_rank', models.CharField(blank=True, max_length=20, null=True)),
                ('volume', models.CharField(blank=True, max_length=20, null=True)),
                ('volume_rank', models.CharField(blank=True, max_length=20, null=True)),
                ('volume_change', models.CharField(blank=True, max_length=20, null=True)),
                ('circulating_supply', models.CharField(blank=True, max_length=20, null=True)),
                ('total_supply', models.CharField(blank=True, max_length=20, null=True)),
                ('diluted_market_cap', models.CharField(blank=True, max_length=20, null=True)),
                ('contracts', models.JSONField(blank=True, default=list, null=True)),
                ('official_links', models.JSONField(blank=True, default=list, null=True)),
                ('social', models.JSONField(blank=True, default=list, null=True)),
                ('is_running', models.BooleanField(default=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('selenium_logs', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_list', to='backend.jobs')),
            ],
        ),
    ]
