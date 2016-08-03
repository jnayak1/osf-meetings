# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 22:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.SlugField(max_length=10, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('site', models.URLField(blank=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('event_start', models.DateTimeField(blank=True, null=True)),
                ('event_end', models.DateTimeField(blank=True, null=True)),
                ('submission_start', models.DateTimeField(blank=True, null=True)),
                ('submission_end', models.DateTimeField(blank=True, null=True)),
                ('logo', models.URLField(blank=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
                'permissions': (('view_conference', 'Can view conference'),),
            },
        ),
    ]
