from django.conf.urls import url, include
from conferences import views

urlpatterns = [
    url(r'^$', views.ConferenceList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ConferenceDetail.as_view(), name='detail'),
    url(r'^(?P<conference_id>[0-9]+)/submissions/',
        include('submissions.urls', namespace='submissions')),
]
