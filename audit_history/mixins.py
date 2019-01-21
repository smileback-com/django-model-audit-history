from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils import timezone

from .fields import AuditHistoryField


class UpdateableModelMixin(object):
    def update(instance, already_set=None, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(instance, k, v)
        updated_fields = kwargs.keys()
        if already_set:
            updated_fields.extend(already_set)
        instance.save(update_fields=updated_fields)
        return instance


class AuditHistoryMixin(UpdateableModelMixin):
    def __init__(self):
        assert isinstance(self, models.Model), 'Mixin has to be attached to a model class'
        try:
            history_field = self._meta.get_field('history')
        except FieldDoesNotExist:
            assert False, 'Mixin has to be attached to a model class with a "history" AuditHistoryField'
        assert isinstance(history_field, AuditHistoryField), 'Mixin has to be attached to a model class with a "history" AuditHistoryField'

    def _create_history_entry(self, modification_time, current_user, event, **payload):
        entry = {'timestamp': modification_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00'),
                 'event': event,
                 'actor': None if not current_user or current_user.is_anonymous() else {'id': current_user.id, 'email': current_user.email, 'name': current_user.get_full_name(), 'is_staff': current_user.is_staff}}
        entry.update(payload)
        return entry

    def _manipulate_model(self, current_user, event, track_last_modification, **payload):
        modification_time = timezone.now()
        if track_last_modification:
            self.last_modified = modification_time
        self.history.append(self._create_history_entry(modification_time, current_user, event, **payload))

    def save_with_audit_record(self, current_user, event, track_last_modification=False, **payload):
        self._manipulate_model(current_user, event, track_last_modification, **payload)
        self.save()

    def update_with_audit_record(self, current_user, event, track_last_modification=False, **fields):
        self._manipulate_model(current_user, event, track_last_modification, **{k: unicode(v) for k, v in fields.items()})
        self.update(already_set=['history'] + (['last_modified'] if track_last_modification else []), **fields)

    def append_audit_record(self, current_user, event, **payload):
        self._manipulate_model(current_user, event, track_last_modification=False, **payload)
        self.save(update_fields=['history'])
