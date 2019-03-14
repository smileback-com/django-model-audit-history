import six
import json

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils import timezone

from .utils import json_formatter
from .fields import AuditHistoryField
from .settings import (
    TIMESTAMP_FORMAT,
    ADMIN_EVENT
)


class UpdateableModelMixin(object):
    def update(self, already_set=None, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)
        updated_fields = list(kwargs.keys())
        if already_set:
            updated_fields.extend(already_set)
        self.save(update_fields=updated_fields)
        return self


class AuditHistoryMixin(UpdateableModelMixin):
    def __init__(self):
        assert isinstance(self, models.Model), 'Mixin has to be attached to a model class'
        try:
            history_field = self._meta.get_field('history')
        except FieldDoesNotExist:
            assert False, 'Mixin has to be attached to a model class with a "history" AuditHistoryField'
        assert isinstance(history_field, AuditHistoryField),\
            'Mixin has to be attached to a model class with a "history" AuditHistoryField'

    @staticmethod
    def _create_history_entry(modification_time, current_user, event, **payload):
        entry = {'timestamp': modification_time.strftime(TIMESTAMP_FORMAT),
                 'event': event,
                 'actor': None if not current_user or current_user.is_anonymous()
                 else {
                     'id': current_user.id,
                     'email': current_user.email,
                     'name': current_user.get_full_name(),
                     'is_staff': current_user.is_staff
                 }}
        payload = json.loads(json.dumps(payload, default=json_formatter))
        entry.update(payload)
        return entry

    def _manipulate_model(self, current_user, event, track_last_modification, **payload):
        modification_time = timezone.now()
        if track_last_modification:
            self.last_modified = modification_time
        self.history.append(self._create_history_entry(modification_time, current_user, event, **payload))

    def save_with_audit_record(self, current_user, event, track_last_modification=False, **payload):
        """
        Saves instance with audit record
        obj.history = [{'timestamp': '%Y-%m-%dT%H:%M:%S.%f+00:00', 'event': 'str', 'actor':
         {'id': 1, 'email': 'example@domain.com', 'name': 'str', 'is_staff': True},
         'payload': {'str': 'str', ...}]
        """
        self._manipulate_model(current_user, event, track_last_modification, **payload)
        self.save()

    def update_with_audit_record(self, current_user, event, track_last_modification=False, **fields):
        """
        Updates instance with audit record
        obj.history = [{'timestamp': '%Y-%m-%dT%H:%M:%S.%f+00:00', 'event': 'str',
         'actor': {'id': 1, 'email': 'example@domain.com', 'name': 'str', 'is_staff': True},
         'field': 'str', ...}]
        """
        self._manipulate_model(current_user, event, track_last_modification,
                               **{k: six.text_type(v) for k, v in fields.items()})
        self.update(already_set=['history'] + (['last_modified'] if track_last_modification else []), **fields)

    def append_audit_record(self, current_user, event, **payload):
        """
        Adds audit record to instance
        obj.history = [{'timestamp': '%Y-%m-%dT%H:%M:%S.%f+00:00', 'event': 'str',
         'actor': {'id': 1, 'email': 'example@domain.com', 'name': 'str', 'is_staff': True},
         'payload': {'str': 'str', ...}}]
        """
        self._manipulate_model(current_user, event, track_last_modification=False, **payload)
        self.save(update_fields=['history'])


class AuditHistoryParentInlineMixin(object):
    """
    Used for admin models which have inline models
    """

    def save_formset(self, request, form, formset, change):
        """
        Save inline models with audit history
        """
        for form in formset.forms:
            if not form.instance.pk or not form.changed_data:
                continue
            form_ch_data = dict(
                (field, form.cleaned_data.get(field)) for field in form.changed_data
            )
            obj = form.save(commit=False)
            if isinstance(obj, AuditHistoryMixin):
                obj.save_with_audit_record(
                    request.user, ADMIN_EVENT,
                    track_last_modification=True,
                    changes=form_ch_data
                )
        super(AuditHistoryParentInlineMixin, self).save_formset(request, form, formset, change)


class AuditHistoryAdminMixin(object):
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
            obj.save_with_audit_record(request.user, ADMIN_EVENT, track_last_modification=True, changes=dict(
                (field, form.cleaned_data.get(field)) for field in form.changed_data
            ))
        else:
            return super(AuditHistoryAdminMixin, self).save_model(request, obj, form, change)
