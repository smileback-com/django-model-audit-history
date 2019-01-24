from django.contrib import admin
from audit_history.admin import AuditHistoryAdmin

from test_app.models import BlogPost


admin.site.register(BlogPost, AuditHistoryAdmin)
