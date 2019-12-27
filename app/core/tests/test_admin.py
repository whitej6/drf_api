from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    """

    """

    def setUp(self):
        """

        """

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@ntc.com',
            password='password'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user@ntc.com',
            password='password',
            name='foo'
        )

    def test_users_listed(self):
        """

        """

        url = reverse('admin:core_user_changelist')
        r = self.client.get(url)

        self.assertContains(r, self.user.name)
        self.assertContains(r, self.user.email)

    def test_user_change_page_renders(self):
        """

        """

        url = reverse("admin:core_user_change", args=[self.user.id])
        r = self.client.get(url)

        self.assertEqual(r.status_code, 200)
