# This snippet goes somewhere inside your project,
# wherever you need to react to incoming emails.
from django_inbound_email.signals import email_received
from views import respond_to_email_submission


def on_email_received(sender, **kwargs):
    """Handle inbound emails."""
    email = kwargs.pop('email')
    respond_to_email_submission(email)

# pass dispatch_uid to prevent duplicates:
# https://docs.djangoproject.com/en/dev/topics/signals/
email_received.connect(on_email_received, dispatch_uid="something_unique")
