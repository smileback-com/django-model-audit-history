from django.contrib import admin

from audit_history.mixins import AuditHistoryMixin
from audit_history.settings import ADMIN_EVENT


class AuditHistoryAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if request.method == 'POST':
            return self.readonly_fields + ('history',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.id and isinstance(obj, AuditHistoryMixin) \
                and form.changed_data:
            obj.save_with_audit_record(request.user, ADMIN_EVENT, payload=form.cleaned_data)
        else:
            return super(AuditHistoryAdmin, self).save_model(request, obj, form, change)
