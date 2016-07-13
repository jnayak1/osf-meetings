from rest_framework_json_api import serializers
from rest_framework.reverse import reverse

from conferences.models import Conference

class ConferenceSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Conference

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse(
                'conferences:detail',
                kwargs={'pk': obj.pk},
                request=request
            ),
            'submissions': reverse(
                'conferences:submissions:list',
                kwargs={'conference_id': obj.pk},
                request=request
            )
        }
