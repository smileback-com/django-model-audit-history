import datetime

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe

from .settings import (
    HISTORY_FIELD_VIEW,
    TIMESTAMP_FORMAT,
    DEFAULT_ACTOR
)


class AuditHistoryWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, list):
            history = reversed(value)
            rows = [HISTORY_FIELD_VIEW.format(
                        timestamp=datetime.datetime.strptime(
                            entry.get('timestamp', '1900-01-01T00:00:00.000+00:00'),
                            TIMESTAMP_FORMAT
                        ),
                        actor=entry['actor'].get('email', '[n/a]') if entry.get('actor') else DEFAULT_ACTOR,
                        event=entry.get('event', '[n/a]'),
                        payload='<br>'.join(['%s=%s' % (k, v)
                                             for k, v in sorted(entry.items())
                                             if k not in ('timestamp', 'actor', 'event',)])
                    ) for entry in history]

            return mark_safe('<table>' + ''.join(rows) + '</table>')

        raise Exception('Unexpected type to render: ' + str(type(value)))
