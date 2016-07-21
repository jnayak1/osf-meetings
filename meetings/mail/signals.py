# This snippet goes somewhere inside your project,
# wherever you need to react to incoming emails.
import logging
from django_inbound_email.signals import email_received
from django.core.files.uploadedfile import SimpleUploadedFile
import requests

from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file


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
    try:
        # create/get user
        pass
    except Exception, e:
        print('Could not create user')
        return
    try:
        # get conference
        pass
    except Exception, e:
        print('Conference does not exist')
        return
    try:
        # post to /submissions
        pass
    except Exception, e:
        print('Invalid submission')
        return
    # send confirmation email
    msg = EmailMultiAlternatives(
        subject="Your submission was sucessful",
        body="Congrats! Your submission here: ",
        from_email="Example <admin@example.com>",
        to=[from_email, ],
        reply_to=["Helpdesk <support@example.com>"])

    # Include an inline image in the html:
    logo_cid = attach_inline_image_file(msg, "/path/to/logo.jpg")
    html = """<img alt="Logo" src="cid:{logo_cid}">
	          <p>Please <a href="http://example.com/activate">activate</a>
	          your account</p>""".format(logo_cid=logo_cid)
    msg.attach_alternative(html, "text/html")

    # Optional Anymail extensions:
    msg.metadata = {}
    msg.tags = []
    msg.track_clicks = True

    # Send it:
    msg.send()


# pass dispatch_uid to prevent duplicates:
# https://docs.djangoproject.com/en/dev/topics/signals/
email_received.connect(on_email_received, dispatch_uid="something_unique")
