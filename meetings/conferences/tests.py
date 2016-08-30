from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from django.conf import settings
import factory
from permissions import ConferencePermissions
from serializers import ConferenceSerializer
from test_factories import UserFactory, ConferenceFactory, SubmissionFactory
from conferences.models import Conference
from views import ConferenceViewSet


class TestPermissions(TestCase):

    def setUp(self):
        self.user1 = UserFactory(
            username='user1'
        )
        self.user2 = UserFactory(
            username='user2'
        )
        group = Group.objects.get(name=settings.HUMANS_GROUP_NAME)
        group.user_set.add(self.user2)
        self.joe = UserFactory(username='joe')
        group.user_set.add(self.joe)
        self.public = User.objects.get(username="AnonymousUser")
        self.conference = ConferenceFactory(
            admin=self.user1,
            id='conferenceId'
        )
        self.submission = SubmissionFactory(
            contributor=self.user2,
            conference=self.conference,
        )

    def test_admin_permissions(self):
        self.assertTrue(
            self.user1.has_perm('change_conference', self.conference)
        )
        self.assertTrue(
            self.user1.has_perm('view_conference', self.conference)
        )
        self.assertTrue(
            self.user1.has_perm('delete_conference', self.conference)
        )

    def test_contributor_permissions(self):
        self.assertFalse(
            self.user2.has_perm('change_conference', self.conference)
        )
        self.assertTrue(
            self.user2.has_perm('view_conference', self.conference)
        )
        self.assertFalse(
            self.user2.has_perm('delete_conference', self.conference)
        )

    def test_logged_in_permissions(self):
        self.assertFalse(
            self.joe.has_perm('change_conference', self.conference)
        )
        self.assertTrue(
            self.joe.has_perm('view_conference', self.conference)
        )
        self.assertFalse(
            self.joe.has_perm('delete_conference', self.conference)
        )

    def test_public_permissions(self):
        self.assertFalse(
            self.public.has_perm('change_conference', self.conference)
        )
        self.assertTrue(
            self.public.has_perm('view_conference', self.conference)
        )
        self.assertFalse(
            self.public.has_perm('delete_conference', self.conference)
        )


class TestSerializers(TestCase):

    def setUp(self):
        self.user1 = UserFactory(
            username='Leo'
        )
        self.user2 = UserFactory(
            username='LeoLeo'
        )
        self.conference = ConferenceFactory(
            id='38',
            admin=self.user1
        )
        self.request1 = RequestFactory().post('./fake_path')
        self.request1.user = self.user1
        self.request1.query_params = {}
        self.request2 = RequestFactory().post('./fake_path')
        self.request2.user = self.user2
        self.request2.query_params = {}

    def test_get_links(self):
        self.serializer = ConferenceSerializer(
            context={'request': self.request1})
        self.links = self.serializer.get_links(self.conference)
        self.assertEqual(
            self.links['self'], 'http://testserver/conferences/38/')
        self.assertEqual(self.links['submissions'],
                         'http://testserver/submissions/?conference=38')

    def test_get_submission_count(self):
        self.submission1 = SubmissionFactory(
            conference=self.conference,
            contributor=factory.SubFactory(UserFactory, username='Tom')
        )
        self.submission2 = SubmissionFactory(
            conference=self.conference,
            contributor=factory.SubFactory(UserFactory, username='User2')
        )
        self.serializer = ConferenceSerializer()
        self.assertEqual(
            self.serializer.get_submission_count(self.conference), 2)
        self.assertFalse(
            self.serializer.get_submission_count(self.conference) == 5)

    def test_get_can_edit(self):
        self.serializer1 = ConferenceSerializer(
            context={'request': self.request1})
        self.serializer2 = ConferenceSerializer(
            context={'request': self.request2})
        self.canEdit1 = self.serializer1.get_can_edit(self.conference)
        self.canEdit2 = self.serializer2.get_can_edit(self.conference)
        self.assertTrue(self.canEdit1)
        self.assertFalse(self.canEdit2)


class TestSignals(TestCase):

    def setUp(self):
        self.user = UserFactory(
            username="Leo"
        )
        self.request = RequestFactory().get('./fake_path')
        self.request.user = self.user
        self.conference = ConferenceFactory(
            admin=self.user
        )

    def test_add_permissions(self):
        self.conference.save()  # This calls add_permission
        self.view = ConferenceViewSet()
        self.request.user = self.user
        self.confPermissions = ConferencePermissions()
        self.assertTrue(self.confPermissions.has_permission(
            self.request, self.view))


class TestViews(TestCase):

    def setUp(self):
        self.user = UserFactory(
            username='testViewsUser'
        )
        self.request = RequestFactory().post('./fake_path')
        self.request.user = self.user
        self.request.query_params = {}
        self.request.data = {
            'id': 's72bc',
            'title': 'conference',
            'city': 'Charlottesville',
            'state': 'Virginia',
            'country': 'NZ'
        }
        self.serializer = ConferenceSerializer(
            context={'request': self.request},
            data=self.request.data
        )
        self.view = ConferenceViewSet()
        self.view.request = self.request
        self.view.format_kwarg = ''

    def test_create(self):
        self.view.create(self.request)
        self.conference = Conference.objects.get(admin=self.user)
        self.assertEqual(self.conference.title, 'conference')

    def test_perform_create(self):
        self.view.perform_create(self.serializer)
        self.conference = Conference.objects.get(admin=self.user)
        self.assertEqual(self.conference.title, 'conference')
