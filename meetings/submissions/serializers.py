from rest_framework_json_api import serializers as ser
from rest_framework.reverse import reverse
from rest_framework_json_api.relations import ResourceRelatedField

from submissions.models import Submission
from approvals.models import Approval
from django.contrib.auth.models import User


class SubmissionSerializer(ser.ModelSerializer):
    links = ser.SerializerMethodField()
    can_edit = ser.SerializerMethodField()
    node_id = ser.CharField(read_only=True)
    contributor = ResourceRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True)
    approval = ResourceRelatedField(
        queryset=Approval.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Submission

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse(
                'submissions:detail',
                kwargs={
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

    def get_can_edit(self, obj):
        request = self.context.get('request')
        user = request.user
        return (user == obj.contributor or user == obj.conference.admin)
