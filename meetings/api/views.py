from django.contrib.auth.models import User, Group
from api.models import Submission, Conference
from api.serializers import UserSerializer, GroupSerializer
from rest_framework import generics, viewsets
from api.serializers import SubmissionSerializer, ConferenceSerializer, AuthenticationSerializer

from rest_framework_json_api.parsers import JSONParser as JSONAPIParser
import requests
from requests_oauth2 import OAuth2
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import authenticate, login
from rest_framework import status


# {user_id : response_from_osf_oauth_post}
# https://github.com/CenterForOpenScience/cas-overlay#authorization-code-exchange
USER_STORAGE = {}

## List of conferences
class ConferenceList(generics.ListCreateAPIView):
    resource_name = 'conferences'
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer

## Detail of a conference
class ConferenceDetail(APIView):
    def get_object(self, pk):
        try:
            return Conference.objects.get(pk=pk)
        except Conference.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conference = self.get_object(pk)
        serializer = ConferenceSerializer(conference)
        return Response(serializer.data)

## List of submissions
class SubmissionList(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    resource_name = 'Submission'
    encoding = 'utf-8'
    queryset= Submission.objects.all()

    def get(self, request, conference_id=None, format=None):
        conferenceSubmissions = Submission.objects.filter(conference_id=conference_id)
        submissionsSerializer = SubmissionSerializer(conferenceSubmissions, context={'request': request}, many=True)
        return Response(submissionsSerializer.data)

    def post(self, request, conference_id=None, format=None):
        serializer = SubmissionSerializer(data=request.data)
        contributors = [request.user.id]

        if serializer.is_valid():
            serializer.save(contributors=contributors)
            return Response(serializer.data)

        return Response(serializer.errors)

## Detail of a submission
class SubmissionDetail(APIView):
    resource_name = 'Submission'
    serializer_class = SubmissionSerializer

    def get(self, request, conference_id=None, submission_id=None , format=None):
        conferenceSubmission = Submission.objects.get(pk=submission_id)
        submissionsSerializer = SubmissionSerializer(conferenceSubmission, context={'request': request}, many=False)
        return Response(submissionsSerializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserDetail(APIView):
    resource_name = 'User'
    serializer_class = UserSerializer

    def get(self, request, user_id=None, format=None):
        user = User.objects.get(pk=user_id)
        userSerializer = UserSerializer(user, context={'request': request}, many=False)
        return Response(userSerializer.data)
