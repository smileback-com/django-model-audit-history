from jsonfield import JSONField
from jsonfield.forms import JSONFormField

from audit_history.widgets import AuditHistoryWidget


class AuditHistoryField(JSONField):
    def __init__(self, *args, **kwargs):
        # override some essential fields
        # if 'null' in kwargs: raise ValueError('Overriding null is not allowed on AuditHistoryFields')
        # if 'default' in kwargs: raise ValueError('Overriding default is not allowed on AuditHistoryFields')
        kwargs['null'] = False
        kwargs['default'] = list
        super(AuditHistoryField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': JSONFormField,
            'widget': AuditHistoryWidget,
        }
        defaults.update(**kwargs)
        return super(AuditHistoryField, self).formfield(**defaults)
