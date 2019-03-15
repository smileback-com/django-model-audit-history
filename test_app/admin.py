from django.contrib import admin
from audit_history.mixins import AuditHistoryAdminMixin

from test_app.models import BlogPost


class BlogPostAdmin(AuditHistoryAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'position')


admin.site.register(BlogPost, BlogPostAdmin)
