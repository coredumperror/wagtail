from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore.models import Group


class TestGroupAdminViewRestrictions(TestCase, WagtailTestUtils):
    """
    Test to make sure users are not being shown groups over which they have no permissions for.
    This uses a custom set of users and groups as follows:

    GROUP  : USER
    =============
    Group A: test1
    Group B: test1, test2
    Group C: test1
    """
    fixtures = ['test_group_restrictions.json']

    def test_admin_sees_all_groups(self):
        self.assertTrue(self.client.login(username='test1', password='asdf'))
        response = self.client.get(reverse('wagtailgroups'))
        pass

    def user_sees_only_permitted_groups(self):
        pass

