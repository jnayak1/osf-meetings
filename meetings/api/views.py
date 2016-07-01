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

CLIENT_ID  = 'daa66c0ca55744cea4600e464fe521ac'
CLIENT_SECRET = 'VX2DTjkfvTEMl1HBgsiav3vBYViWgzUwMWgVg8nw'
REDIRECT_URI = "http://localhost:4200/login"
OSF_API_URL = "https://test-api.osf.io/"
OSF_ACCOUNTS_URL = "https://test-accounts.osf.io/"

class OsfAuthorizationCode(APIView):
    def get(self, request, format=None):
        code = request.GET.get('code')
        if code != None:
            post_data = { "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
            oauth_response = requests.post(OSF_ACCOUNTS_URL + "oauth2/token", data=post_data)
            try:
                headers = {'Authorization': 'Bearer ' + oauth_response.json()['access_token']}
                osf_user = requests.get(OSF_API_URL + 'v2/users/me', headers=headers).json()
                osf_uid = osf_user['data']['id']
                USER_STORAGE[osf_uid] = oauth_response
                user = authenticate(username=osf_uid, password='secret')
            except KeyError, e:
                return Response("Invalid OAUTH code",  status=status.HTTP_404_NOT_FOUND)
            if user:
                # if user already has an account, log them in
                login(request,user)
            else:
                # else, create account for user, log them in
                User.objects.create_user(username=osf_uid, password='secret')
                user = authenticate(username=osf_uid, password='secret')
                login(request,user)
            # returning token for now for easy testing
            return Response(oauth_response.json()['access_token'], status=status.HTTP_200_OK)
        else:
            return Response("Invalid OAUTH code",  status=status.HTTP_404_NOT_FOUND)
        

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
