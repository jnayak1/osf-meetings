from django.conf.urls import url, include
from api import views as apiViews
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from rest_framework import routers

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = routers.DefaultRouter()
router.register(r'users', apiViews.UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^conferences/', include('conferences.urls', namespace='conferences')),
    url(r'^checklogin/', apiViews.checkLoggedIn.as_view(), name='checklogin'), 
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
