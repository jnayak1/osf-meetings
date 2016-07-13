from rest_framework_json_api import serializers as ser
from rest_framework.reverse import reverse

from submissions.models import Submission
from conferences.models import Conference
from api.serializers import UserSerializer


class SubmissionSerializer(ser.ModelSerializer):
    links = ser.SerializerMethodField()
    contributors = UserSerializer(many=True)
    node_id = ser.CharField(read_only=True)

    def create(self, validated_data):
        # look up contributors by ID
        contributors = validated_data['contributors']
        title = validated_data['title']
        description = validated_data['description']
        conference = validated_data['conference']
        submission = Submission.objects.create(title=title, description=description, conference=conference, approved=False)
        for contributor in contributors:
                submission.contributors.add(contributor)
        return submission

    class Meta:
        model = Submission
        fields = ('id', 'node_id', 'title', 'description', 'conference',
                  'contributors', 'links')

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse(
                'conferences:submissions:detail',
                kwargs={
                    'conference_id': obj.conference.id,
                    'submission_id': obj.pk
                },
                request=request
            ),
            'conference': reverse(
                'conferences:detail',
                kwargs={'pk': obj.conference.id},
                request=request
            ),
        }
