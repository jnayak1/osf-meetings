# This snippet goes somewhere inside your project,
# wherever you need to react to incoming emails.
import logging
from django_inbound_email.signals import email_received
from django.core.files.uploadedfile import SimpleUploadedFile
import requests

from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file
from mail.mails import SubmissionSuccessEmail, SubmissionConfDNE, SubmissionWithoutFiles
from django.conf import settings
from conferences.models import Conference


def get_file(attachment):
    """Convert email.attachment tuple into a SimpleUploadedFile."""
    name, content, content_type = attachment
    return SimpleUploadedFile(name, content, content_type)


def on_email_received(sender, **kwargs):
    """Handle inbound emails."""
    email = kwargs.pop('email')
    title = email.subject
    submission_description = email.body
    submitter_email = email.from_email
    conference_email = email.to[0]
    files = []
    for attachment in email.attachments:
        # we must convert attachment tuple into a file
        # before adding as the property.
        file = get_file(attachment)
        files.append(file)

    conf_identifier = conference_email.strip('-poster@osf.io').strip('-talk@osf.io')
    # create/get user
    # get conference
    print(str(files))
    try:
    	conf = Conference.objects.get(id=conf_identifier)
    	if not files:
    		raise ValueError('No file attachments')
    except Conference.DoesNotExist, e:
    	msg = SubmissionConfDNE(to=submitter_email, from_email=conference_email)
    	# msg.send()
    except ValueError, e:
    	msg = SubmissionWithoutFiles(to=submitter_email, from_email=conference_email)
    	# msg.send()
    else:
    	# post submission
	    # send confirmation email
	    msg = SubmissionSuccessEmail(to=submitter_email, from_email=conference_email, conf_full_name='',
	                 presentation_type='', node_url='', conf_view_url='',
	                 fullname='', user_created=True, is_spam=False, profile_url='')
	    # msg.send()

# pass dispatch_uid to prevent duplicates:
# https://docs.djangoproject.com/en/dev/topics/signals/
email_received.connect(on_email_received, dispatch_uid="something_unique")
