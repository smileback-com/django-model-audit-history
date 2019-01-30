from .main import BaseTestSetUp
from test_app.forms import BlogPostForm

from audit_history.utils import json_formatter


class AuditHistoryFormTest(BaseTestSetUp):
    def setUp(self):
        super(AuditHistoryFormTest, self).setUp()
        self.form = BlogPostForm({
            'title': self.blog_title,
            'position': self.blog_position,
            'created_on': self.blog_created
        })

    def test_form_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_save_with_audit(self):
        self.form.save(commit=True)
        self.assertFalse(self.form.errors)
        self.blog_post.save_with_audit_record(None, self.history_event, payload=self.form.cleaned_data)
        self.assertNotEqual([], self.blog_post.history)
        self.assertEqual(self.history_event, self.blog_post.history[0]['event'])
        self.assertEqual(None, self.blog_post.history[0]['actor'])
        self.assertEqual(self.blog_title, self.blog_post.history[0]['payload']['title'])
        self.assertEqual(self.blog_position, self.blog_post.history[0]['payload']['position'])
        self.assertEqual(json_formatter(self.blog_created), self.blog_post.history[0]['payload']['created_on'])
