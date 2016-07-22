# This snippet goes somewhere inside your project,
# wherever you need to react to incoming emails.
import logging
from django_inbound_email.signals import email_received
from django.core.files.uploadedfile import SimpleUploadedFile
import requests

from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file
from mail.mails import SubmissionSuccessEmail
from django.conf import settings
from conferences.models import Conference


def get_file(attachment):
    """Convert email.attachment tuple into a SimpleUploadedFile."""
    name, content, content_type = attachment
    return SimpleUploadedFile(name, content, content_type)


def on_email_received(sender, **kwargs):
    """Handle inbound emails."""
    email = kwargs.pop('email')
    subject = email.subject
    body = email.body
    from_email = email.from_email
    to = email.to
    files = []
    for attachment in email.attachments:
        # we must convert attachment tuple into a file
        # before adding as the property.
        file = get_file(attachment)
        files.append(file)

    conf_identifier = to[0].strip('@osf.io').strip('poster').strip('talk')[:-1]
    conf = Conference.objects.get(id=conf_identifier)

    # create/get user
    # get conference
    # post to /submissions

    # send confirmation email
    
    

    msg = SubmissionSuccessEmail(send_to=from_email, from_email=to[0], conf_full_name='',
                 presentation_type='', node_url='', conf_view_url='',
                 fullname='', user_created=True, is_spam=False, profile_url='')
    # msg.send()

# pass dispatch_uid to prevent duplicates:
# https://docs.djangoproject.com/en/dev/topics/signals/
email_received.connect(on_email_received, dispatch_uid="something_unique")
