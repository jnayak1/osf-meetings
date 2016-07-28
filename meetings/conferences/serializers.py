from rest_framework_json_api import serializers
from rest_framework.reverse import reverse

from conferences.models import Conference
from submissions.models import Submission
from django.contrib.auth.models import User

from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr


class Base64ImageField(serializers.ImageField):

    """
    From http://stackoverflow.com/q/28036404
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ConferenceSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    submission_count = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    admin = serializers.PrimaryKeyRelatedField(read_only=True)
    logo = Base64ImageField()

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
            'submissions': '{}?conference={}'.format(
                reverse('submissions:list', request=request),
                obj.pk
            )
        }

    def get_submission_count(self, obj):
        return len(Submission.objects.filter(conference=obj))

    def get_can_edit(self, obj):
        request = self.context.get('request')
        user = User.objects.get(username=request.user)
        return user == obj.admin
