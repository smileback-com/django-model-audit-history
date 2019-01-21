import datetime
import json

from django.forms.widgets import Widget
from jsonfield.utils import default


class AuditHistoryWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        # TODO: I have no idea why this comes in as unicode after a POST
        if isinstance(value, unicode):
            value = json.loads(value)

        if isinstance(value, list):
            history = reversed(value)
            rows = ['<tr><td>{timestamp:%Y-%m-%d %H:%M:%S} UTC</td><td>{actor}</td><td>{event}</td><td>{payload}</td></tr>'.format(
                        timestamp=datetime.datetime.strptime(entry.get('timestamp', '1900-01-01T00:00:00.000Z'), '%Y-%m-%dT%H:%M:%S.%fZ'),
                        actor=entry['actor'].get('email', '[n/a]') if entry.get('actor') else 'System',
                        event=entry.get('event', '[n/a]'),
                        payload='<br>'.join(['%s=%s' % (k, v) for k, v in sorted(entry.items()) if k not in ('timestamp', 'actor', 'event',)])
                    ) for entry in history]

            # looking for a more elegant solution to take this field out of the UPDATE flow, but this works for now
            hidden_field = '<input type="hidden" name="%s" value=\'%s\'></input>' % (name, json.dumps(value, default=default))

            return '<table>' + ''.join(rows) + '</table>' + hidden_field

        raise Exception('Unexpected type to render: ' + str(type(value)))
