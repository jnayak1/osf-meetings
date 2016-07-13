from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import filters 
from conferences.models import Conference
from conferences.serializers import ConferenceSerializer


# List of conferences
class ConferenceList(ListCreateAPIView):
    resource_name = 'conferences'

    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description')


# Detail of a conference
class ConferenceDetail(APIView):
    resource_name = 'conference'

    def get_object(self, pk):
        try:
            return Conference.objects.get(pk=pk)
        except Conference.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conference = self.get_object(pk)
        serializer = ConferenceSerializer(conference)
        return Response(serializer.data)
