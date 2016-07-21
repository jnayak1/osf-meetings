# This snippet goes somewhere inside your project,
# wherever you need to react to incoming emails.
import logging
from django_inbound_email.signals import email_received
from django.core.files.uploadedfile import SimpleUploadedFile


def get_file(attachment):
    """Convert email.attachment tuple into a SimpleUploadedFile."""
    name, content, content_type = attachment
    return SimpleUploadedFile(name, content, content_type)


def on_email_received(sender, **kwargs):
    """Handle inbound emails."""
    email = kwargs.pop('email')
    for attachment in email.attachments:
        # we must convert attachment tuple into a file
        # before adding as the property.
        file = get_file(attachment)
        # do something with file

# pass dispatch_uid to prevent duplicates:
# https://docs.djangoproject.com/en/dev/topics/signals/
email_received.connect(on_email_received, dispatch_uid="something_unique")
