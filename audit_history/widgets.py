import json

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.utils.dateparse import parse_datetime
from django.template.loader import render_to_string

from .settings import DEFAULT_ACTOR


class AuditHistoryWidget(Widget):
    """
    Custom widget for AuditHistoryField
    """
    template_name = 'widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, str):
            history = reversed(json.loads(value))
            rows = [{
                    'timestamp': parse_datetime(entry.get('timestamp', '1900-01-01T00:00:00.000+00:00')),
                    'actor': entry['actor'].get('email', '[n/a]') if entry.get('actor') else DEFAULT_ACTOR,
                    'event': entry.get('event', '[n/a]'),
                    'payload':['%s=%s' % (k, v) for k, v in sorted(entry.items())
                               if k not in ('timestamp', 'actor', 'event',)]
                    } for entry in history]

            return mark_safe(render_to_string(self.template_name, {'data': rows}))

        raise Exception('Unexpected type to render: ' + str(type(value)))
