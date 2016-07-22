from django.core.mail.message import EmailMultiAlternatives
from django.template import Context, Template
from django.template.loader import get_template


class SubmissionSuccessEmail(EmailMultiAlternatives):

    def __init__(self, to=None, from_email=None, conf_full_name='',
                 presentation_type='', node_url='', conf_view_url='',
                 fullname='', user_created=True, is_spam=False, profile_url=''):

        subject = "Your submission to OSF for Meetings was succesful"

        super(SubmissionSuccessEmail, self).__init__(subject=subject,
                                                     to=[to],
                                                     from_email=from_email)
        success_template = get_template('conference_submitted.mako')
        success_context = Context({'conf_full_name': conf_full_name,
                                   'presentation_type': presentation_type,
                                   'set_password_url': '',
                                   'profile_url': profile_url,
                                   'user_created': user_created,
                                   'node_url': node_url,
                                   'conf_view_url': conf_view_url,
                                   'is_spam': is_spam,
                                   'fullname': fullname,
                                   })
        rendered_success_template = success_template.render(success_context)
        print(rendered_success_template)
        self.attach_alternative(rendered_success_template, "text/html")


class SubmissionConfDNE(EmailMultiAlternatives):

    def __init__(self, to=None, from_email=None, fullname=''):
        super(SubmissionConfDNE, self).__init__()

        subject = "There was an error with your submission to OSF for Meetings"
        dne_template = get_template('conference_does_not_exist.mako')
        dne_context = Context({'fullname': fullname, })
        rendered_dne_template = dne_template.render(dne_context)
        print(rendered_dne_template)
        self.attach_alternative(rendered_dne_template, "text/html")


class SubmissionWithoutFiles(EmailMultiAlternatives):

    def __init__(self, to=None, from_email=None, fullname=''):
        super(SubmissionWithoutFiles, self).__init__()

        subject = "There was an error with your submission to OSF for Meetings"
        dne_template = get_template('conference_without_files.mako')
        dne_context = Context({'fullname': fullname, })
        rendered_dne_template = dne_template.render(dne_context)
        print(rendered_dne_template)
        self.attach_alternative(rendered_dne_template, "text/html")
