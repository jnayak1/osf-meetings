from django.core.mail.message import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


class SubmissionSuccessEmail(EmailMultiAlternatives):

    def __init__(self, to=None, from_email=None, conference=None,
                 user=None):
        super(SubmissionSuccessEmail, self).__init__(to=[to],
                                                     from_email=from_email)
        self.subject = "Your submission to OSF for Meetings was succesful!"
        conf_full_name = conference.title
        presentation_type = ''
        set_password_url = ''
        profile_url = ''
        user_created = True
        node_url = ''
        conf_view_url = ''
        is_spam = False
        fullname = 'joe smith'  # get from user when implemented
        success_template = get_template('conference_submitted.html')
        success_context = Context({'conf_full_name': conf_full_name,
                                   'presentation_type': presentation_type,
                                   'set_password_url': set_password_url,
                                   'profile_url': profile_url,
                                   'user_created': user_created,
                                   'node_url': node_url,
                                   'conf_view_url': conf_view_url,
                                   'is_spam': is_spam,
                                   'fullname': fullname,
                                   })
        rendered_success_template = success_template.render(success_context)
        self.attach_alternative(rendered_success_template, "text/html")


class SubmissionConfDNE(EmailMultiAlternatives):

    def __init__(self, to=None, from_email=None, user=None):
        super(SubmissionConfDNE, self).__init__()
        self.subject = "There was an error with your submission to OSF for Meetings"
        fullname = 'joe smith'  # get from user when implemented
        dne_template = get_template('conference_does_not_exist.html')
        dne_context = Context({'fullname': fullname, })
        rendered_dne_template = dne_template.render(dne_context)
        self.attach_alternative(rendered_dne_template, "text/html")


class SubmissionWithoutFiles(EmailMultiAlternatives):

    def __init__(self, to=None, from_email=None, user=None):
        super(SubmissionWithoutFiles, self).__init__()
        self.subject = "There was an error with your submission to OSF for Meetings"
        fullname = 'joe smith'  # get from user when implemented
        template = get_template('conference_without_files.html')
        context = Context({'fullname': fullname, })
        rendered_template = template.render(context)
        self.attach_alternative(rendered_template, "text/html")
