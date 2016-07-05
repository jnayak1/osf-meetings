from django.conf.urls import url
from submissions import views

urlpatterns = [
    url(r'^$', views.SubmissionList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.SubmissionDetail.as_view(), name='detail'),
]
