from django.conf.urls import patterns, include, url

urlpatterns = [
    url(r'^', include('django_inbound_email.urls')),
]
