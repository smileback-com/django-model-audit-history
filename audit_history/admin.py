from django.contrib import admin

from audit_history.mixins import AuditHistoryMixin
from audit_history.settings import ADMIN_EVENT


class AuditHistoryAdmin(admin.ModelAdmin):
    """
    Custom Admin for models with AuditHistoryField
    """

    def get_readonly_fields(self, request, obj=None):
        """
        Sets history field to readonly while instance is updating via admin
        return: self.readonly_fields
        """
        if request.method == 'POST':
            return self.readonly_fields + ('history',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """
        Adds audit history when instance has updated via admin
        """
        if obj.id and isinstance(obj, AuditHistoryMixin) \
                and form.changed_data:
            obj.save_with_audit_record(request.user, ADMIN_EVENT, payload=form.cleaned_data)
        else:
            return super(AuditHistoryAdmin, self).save_model(request, obj, form, change)
