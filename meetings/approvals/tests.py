from django.test import TestCase
from django.contrib.auth.models import User
import test_factories


class TestApproval(TestCase):
    def setUp(self):
        self.user = test_factories.UserFactory(username='admin')
        self.contributor = test_factories.UserFactory(username='contrib')
        self.joe = test_factories.UserFactory(username='joe')
        self.public = User.objects.get(username='AnonymousUser')
        self.approval = test_factories.ApprovalFactory(id=1)
        self.conference = test_factories.ConferenceFactory(admin=self.user)

    def test_signal(self):
        self.assertFalse(self.user.has_perm('change_approval', self.approval))
        test_factories.SubmissionFactory(contributor_id=1,
                                         approval=self.approval,
                                         conference=self.conference)
        self.assertTrue(self.user.has_perm('change_approval', self.approval))

    # @skip('Test that permissions are limited, use as many defs as necessary')
    def _submission(self):
        test_factories.SubmissionFactory(
            contributor=self.contributor,
            approval=self.approval,
            conference=self.conference
        )

    def test_admin_permissions(self):
        self._submission()
        self.assertTrue(self.user.has_perm('change_approval', self.approval))
        self.assertTrue(self.user.has_perm('view_approval', self.approval))
        self.assertTrue(self.user.has_perm('delete_approval', self.approval))

    def test_contributor_permissions(self):
        self._submission()
        self.assertFalse(
            self.contributor.has_perm('change_approval', self.approval)
        )
        self.assertTrue(
            self.contributor.has_perm('view_approval', self.approval)
        )
        self.assertTrue(
            self.contributor.has_perm('delete_approval', self.approval)
        )

    def test_logged_in_permissions(self):
        self._submission()
        self.assertFalse(self.joe.has_perm('change_approval', self.approval))
        self.assertFalse(self.joe.has_perm('view_approval', self.approval))
        self.assertFalse(self.joe.has_perm('delete_approval', self.approval))

    def test_public_permissions(self):
        self._submission()
        self.assertFalse(self.public.has_perm('change_approval', self.approval))
        self.assertFalse(self.public.has_perm('view_approval', self.approval))
        self.assertFalse(self.public.has_perm('delete_approval', self.approval))
