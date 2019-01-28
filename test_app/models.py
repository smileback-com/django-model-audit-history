from django.db import models
from django.utils.timezone import now

from audit_history.fields import AuditHistoryField
from audit_history.mixins import AuditHistoryMixin


class BlogPost(models.Model, AuditHistoryMixin):
    title = models.CharField(max_length=255, blank=False)
    position = models.IntegerField(default=1, blank=False)
    created_on = models.DateTimeField(default=now, blank=True)
    history = AuditHistoryField()

    def __unicode__(self):
        return 'BlogPost {id} @ {position}: {title}'.format(id=self.id, position=self.position, title=self.title)
