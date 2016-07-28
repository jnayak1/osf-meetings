from __future__ import unicode_literals

from django.db import models

from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Conference(models.Model):
    id = models.SlugField(primary_key=True, max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    site = models.URLField(blank=True)
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    country = CountryField()
    event_start = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)
    submission_start = models.DateTimeField(blank=True, null=True)
    submission_end = models.DateTimeField(blank=True, null=True)
    logo = models.ImageField(blank=True, upload_to='conference_logos')
    description = models.TextField(blank=True, max_length=500)
    admin = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        ordering = ('created', )
        permissions = (
            ('view_conference', 'Can view conference'),
        )

    class JSONAPIMeta:
        resource_name = "conferences"
