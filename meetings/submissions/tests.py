from django.test import TestCase, RequestFactory
from collections import OrderedDict
import mock
import factory
from submissions.models import Submission
from django.contrib.auth.models import User, Group
from django.conf import settings
from test_factories import (
    UserFactory, SubmissionFactory, ConferenceFactory,
    SocialAccountFactory, SocialTokenFactory,
    SocialAppFactory, ApprovalFactory, ResponseFactory,
    setup_view_user
)
from serializers import SubmissionSerializer
from views import SubmissionViewSet


class TestApprovedPermissions(TestCase):
    def setUp(self):
        self.user1 = UserFactory(
            username='user1'
        )
        self.user2 = UserFactory(
            username='user2'
        )
        self.joe = UserFactory(username='joe')
        group = Group.objects.get(name=settings.HUMANS_GROUP_NAME)
        group.user_set.add(self.joe)
        self.public = User.objects.get(username='AnonymousUser')
        self.conference = ConferenceFactory(
            admin=self.user1,
            id='conferenceId'
        )
        self.submission = SubmissionFactory(
            contributor=self.user2,
            conference=self.conference,
            approval=factory.SubFactory(ApprovalFactory, approved=True)
        )
        self.submission2 = SubmissionFactory(
            contributor=self.user2,
            conference=self.conference,
            approval=factory.SubFactory(ApprovalFactory, approved=False)
        )

    def test_admin_permission(self):
        self.assertTrue(self.user1.has_perm('view_submission', self.submission))
        self.assertTrue(self.user1.has_perm('change_submission', self.submission))
        self.assertTrue(self.user1.has_perm('delete_submission', self.submission))

    def test_contributor_permission(self):
        self.assertTrue(self.user2.has_perm('view_submission', self.submission))
        self.assertTrue(self.user2.has_perm('change_submission', self.submission))
        self.assertTrue(self.user2.has_perm('delete_submission', self.submission))

    def test_public_permissions(self):
        self.assertTrue(self.public.has_perm('view_submission', self.submission))
        self.assertFalse(self.public.has_perm('change_submission', self.submission))
        self.assertFalse(self.public.has_perm('delete_submission', self.submission))

    def test_logged_in_permissions(self):
        self.assertTrue(self.joe.has_perm('view_submission', self.submission))
        self.assertFalse(self.joe.has_perm('change_submission', self.submission))
        self.assertFalse(self.joe.has_perm('delete_submission', self.submission))

    def test_admin_permission_unapproved(self):
        self.assertTrue(self.user1.has_perm('view_submission', self.submission2))
        self.assertTrue(self.user1.has_perm('change_submission', self.submission2))
        self.assertTrue(self.user1.has_perm('delete_submission', self.submission2))

    def test_contributor_permission_unapproved(self):
        self.assertTrue(self.user2.has_perm('view_submission', self.submission2))
        self.assertTrue(self.user2.has_perm('change_submission', self.submission2))
        self.assertTrue(self.user2.has_perm('delete_submission', self.submission2))

    def test_public_permissions_unapproved(self):
        self.assertFalse(self.public.has_perm('view_submission', self.submission2))
        self.assertFalse(self.public.has_perm('change_submission', self.submission2))
        self.assertFalse(self.public.has_perm('delete_submission', self.submission2))

    def test_logged_in_permissions_unapproved(self):
        self.assertFalse(self.joe.has_perm('view_submission', self.submission2))
        self.assertFalse(self.joe.has_perm('change_submission', self.submission2))
        self.assertFalse(self.joe.has_perm('delete_submission', self.submission2))


class TestSerializers(TestCase):
    def setUp(self):
        self.user = UserFactory(
            username='testUser'
            )
        self.request = RequestFactory().get('./fake_path')
        self.request.query_params = {}
        self.request.user = self.user
        self.submission = SubmissionFactory(
            contributor=self.user,
            conference=factory.SubFactory(ConferenceFactory, id='382',
                                          admin=factory.SubFactory(UserFactory, username='u1'))
            )

    def test_get_links(self):
        serializer = SubmissionSerializer(context={'request': self.request})
        links = serializer.get_links(self.submission)
        self.assertEqual(links['self'], 'http://testserver/submissions/1/')
        self.assertEqual(links['conference'], 'http://testserver/conferences/382/')

    def test_get_can_edit(self):
        serializer = SubmissionSerializer(context={'request': self.request})
        submission2 = SubmissionFactory(
            contributor=factory.SubFactory(UserFactory, username='differentUser'),
            conference=factory.SubFactory(ConferenceFactory, id='234', admin=self.user)
            )
        submission3 = SubmissionFactory(
            contributor=factory.SubFactory(UserFactory, username='differentUser2'),
            conference=factory.SubFactory(ConferenceFactory, id='18',
                                          admin=factory.SubFactory(UserFactory,
                                                                   username='differentUser3'))
            )
        self.assertTrue(serializer.get_can_edit(self.submission))
        self.assertTrue(serializer.get_can_edit(submission2))
        self.assertFalse(serializer.get_can_edit(submission3))


class TestSignals(TestCase):
    def setUp(self):
        self.user1 = UserFactory(
            username='user1'
        )
        self.user2 = UserFactory(
            username='user2'
        )
        self.user3 = User.objects.get(username='AnonymousUser')
        self.conference = ConferenceFactory(
            admin=self.user1,
            id='conferenceId'
        )
        self.submission1 = SubmissionFactory(
            contributor=self.user2,
            conference=self.conference,
            approval=factory.SubFactory(ApprovalFactory, approved=True)
            )
        self.submission2 = SubmissionFactory(
            contributor=self.user2,
            conference=self.conference,
            approval=factory.SubFactory(ApprovalFactory, approved=False)
            )

    def test_add_permissions_approved(self):
        self.submission1.save()
        self.assertTrue(self.user3.has_perm('view_submission', self.submission1))

    def test_add_permissions_rejected(self):
        self.submission2.save()
        self.assertFalse(self.user3.has_perm('view_submission', self.submission2))


class TestViews(TestCase):

    def setUp(self):
        self.user = UserFactory(
            username='testViewsUser',
            id='428'
            )
        self.socialApp = SocialAppFactory()
        self.socialAccount = SocialAccountFactory(
            user=self.user,
            uid='testViewsUser'
            )
        self.socialToken = SocialTokenFactory(
            account=self.socialAccount,
            app=factory.SubFactory(SocialAppFactory),
            token='235387023',
            token_secret='24358103981'
            )
        self.conference = ConferenceFactory(
            admin=self.user,
            id='conferenceId'
            )
        self.request = RequestFactory().post('./fake_path')
        self.request.user = self.user
        self.request.query_params = {}
        self.request.data = {
            u'category': u'project',
            u'can_edit': False,
            u'node_id': None,
            u'description': u'Over subscribed',
            u'title': u'Submission65',
            u'contributor': None,
            u'metafile': None,
            'id': None,
            u'conference': OrderedDict(
                [(u'type', u'conferences'), (u'id', u'conferenceId')])
        }
        self.views = SubmissionViewSet()
        self.views = setup_view_user(self.views, self.request, self.user)

    @mock.patch('submissions.views.requests.post')
    def test_perform_create(self, mock_method):
        mock_method.return_value = ResponseFactory(
            content={'data': {'id': 'qjdfy'}}
            )
        serializer = SubmissionSerializer(data=self.request.data)
        serializer.is_valid()
        self.views.perform_create(serializer)
        self.assertEqual(1, Submission.objects.count())
