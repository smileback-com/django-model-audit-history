from django.test import TestCase
from test_app.models import BlogPost
from django.contrib.auth.models import User
from django.utils import timezone


class BaseTestSetUp(TestCase):

    def setUp(self):
        self.blog_post = BlogPost(title='test', position=1)
        self.user_name = 'test_user'
        self.user_email = 'test@test.domain'
        self.user_password = 'test_password'
        self.history_event = 'test_event'
        self.not_used_timestamp_format = '%Y-%m-%dT%H:%M:%S'
        self.payload = {'a': 'test_history_1', 'b': 'test_history_2'}
        self.payload_with_quotes = {'title': "test'test"}
        self.admin_change_url = 'admin:test_app_blogpost_change'
        self.admin_add_url = 'admin:test_app_blogpost_add'
        self.blog_title = 'test'
        self.blog_position = 1
        self.blog_created = timezone.now()
        self.payload_for_update = {
            'title': 'updated_title',
            'position': 20,
        }
        self.user = User.objects.create_superuser(
            username=self.user_name,
            email=self.user_email,
            password=self.user_password,
            first_name=self.user_name)
