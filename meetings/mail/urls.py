from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('django_inbound_email.urls')),
]
