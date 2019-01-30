from random import randint

from test_app.models import BlogPost
from .main import BaseTestSetUp


class AuditHistoryTest(BaseTestSetUp):

    def test_create_instance(self):
        self.blog_post.save()
        self.assertEqual(1, BlogPost.objects.count())

    def test_empty_history_after_save(self):
        self.blog_post.save()
        self.assertEqual([], self.blog_post.history)

    def test_history_after_save_with_audit(self):
        self.blog_post.save_with_audit_record(None, self.history_event, payload=self.payload)
        self.assertEqual(self.payload['a'], self.blog_post.history[0]['payload']['a'])

    def test_save_with_audit_record_with_staff_user(self):
        self.blog_post.save_with_audit_record(self.user, self.history_event, payload=self.payload)
        self.assertEqual(self.user_name, self.blog_post.history[0]['actor']['name'])
        self.assertEqual(self.user_email, self.blog_post.history[0]['actor']['email'])
        self.assertEqual(True, self.blog_post.history[0]['actor']['is_staff'])
        self.assertEqual(self.payload['a'], self.blog_post.history[0]['payload']['a'])
        self.assertEqual(self.payload['b'], self.blog_post.history[0]['payload']['b'])

    def test_save_with_audit_record_without_user(self):
        self.blog_post.save_with_audit_record(None, self.history_event, payload=self.payload)
        self.assertEqual(None, self.blog_post.history[0]['actor'])
        self.assertEqual(self.payload['a'], self.blog_post.history[0]['payload']['a'])
        self.assertEqual(self.payload['b'], self.blog_post.history[0]['payload']['b'])

    def test_n_usages_of_save_with_audit(self):
        for _ in range(100):
            self.blog_post.save_with_audit_record(None, self.history_event, payload=self.payload)
        self.assertEqual(100, len(self.blog_post.history))

    def test_append_audit_record_with_staff_user(self):
        self.blog_post.save()
        self.blog_post.append_audit_record(self.user, self.history_event, payload=self.payload)
        self.assertEqual(self.user_name, self.blog_post.history[0]['actor']['name'])
        self.assertEqual(self.user_email, self.blog_post.history[0]['actor']['email'])
        self.assertEqual(True, self.blog_post.history[0]['actor']['is_staff'])
        self.assertEqual(self.payload['a'], self.blog_post.history[0]['payload']['a'])
        self.assertEqual(self.payload['b'], self.blog_post.history[0]['payload']['b'])

    def test_append_audit_record_without_user(self):
        self.blog_post.save()
        self.blog_post.append_audit_record(None, self.history_event, payload=self.payload)
        self.assertEqual(None, self.blog_post.history[0]['actor'])
        self.assertEqual(self.payload['a'], self.blog_post.history[0]['payload']['a'])
        self.assertEqual(self.payload['b'], self.blog_post.history[0]['payload']['b'])

    def test_n_usages_of_append_audit_record(self):
        self.blog_post.save()
        for _ in range(100):
            self.blog_post.append_audit_record(None, self.history_event, payload=self.payload)
        self.assertEqual(100, len(self.blog_post.history))

    def test_update_with_audit_record_with_staff_user(self):
        self.blog_post.save()
        self.blog_post.update_with_audit_record(self.user, self.history_event, **self.payload_for_update)
        self.assertEqual(self.user_name, self.blog_post.history[0]['actor']['name'])
        self.assertEqual(self.user_email, self.blog_post.history[0]['actor']['email'])
        self.assertEqual(True, self.blog_post.history[0]['actor']['is_staff'])
        self.assertEqual(self.payload_for_update['title'], self.blog_post.history[0]['title'])
        self.assertEqual(self.payload_for_update['position'], int(self.blog_post.history[0]['position']))

    def test_update_with_audit_record_without_user(self):
        self.blog_post.save()
        self.blog_post.update_with_audit_record(None, self.history_event, **self.payload_for_update)
        self.assertEqual(None, self.blog_post.history[0]['actor'])
        self.assertEqual(self.payload_for_update['title'], self.blog_post.history[0]['title'])
        self.assertEqual(self.payload_for_update['position'], int(self.blog_post.history[0]['position']))

    def test_n_usages_of_update_with_audit_record(self):
        self.blog_post.save()
        for _ in range(100):
            self.blog_post.update_with_audit_record(None, self.history_event, **self.payload_for_update)
        self.assertEqual(100, len(self.blog_post.history))
