from mail.mails import (SubmissionSuccessEmail,
                        SubmissionConfDNE, SubmissionWithoutFiles)
from conferences.models import Conference
import requests  # noqa
from django.core.files.uploadedfile import SimpleUploadedFile


def get_file(attachment):
    """Convert email.attachment tuple into a SimpleUploadedFile."""
    name, content, content_type = attachment
    return SimpleUploadedFile(name, content, content_type)


def respond_to_email_submission(email):
    # title = email.subject
    # submission_description = email.body
    submitter_email = email.from_email
    conference_email = email.to[0]
    files = []
    for attachment in email.attachments:
        # we must convert attachment tuple into a file
        # before adding as the property.
        file = get_file(attachment)
        files.append(file)

    conf_identifier = conference_email.strip(
        '-poster@osf.io').strip('-talk@osf.io')

    msg = ''
    # get/create user
    try:
        conf = Conference.objects.get(id=conf_identifier)
        if not files:
            raise ValueError('No file attachments')
    except Conference.DoesNotExist:
        msg = SubmissionConfDNE(to=submitter_email,
                                from_email=conference_email)
    except ValueError:
        msg = SubmissionWithoutFiles(to=submitter_email,
                                     from_email=conference_email)
    else:
        # post submission here
        msg = SubmissionSuccessEmail(to=submitter_email,
                                     from_email=conference_email,
                                     conference=conf)
    finally:
        print(str(msg))
        # msg.send()
