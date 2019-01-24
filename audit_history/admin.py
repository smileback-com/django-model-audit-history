from django.contrib import admin


class AuditHistoryAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if request.method == 'POST':
            return self.readonly_fields + ('history',)
        return self.readonly_fields
