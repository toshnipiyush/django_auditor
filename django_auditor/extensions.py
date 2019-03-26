from django.db import models

from django_auditor.get_current_user import current_request
from django_auditor.utils import track_audit_logs_entries, create_logs


class AuditLogBaseModel(models.Model):

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        # ToDo: Log entries on delete operation
        request = current_request()
        performed_by = request.user.id if request else None
        entity_logs = track_audit_logs_entries(self, performed_by=performed_by)
        super_data = super(AuditLogBaseModel, self).save(*args, **kwargs)
        create_logs(entity_logs)
        return super_data

    class Meta:
        abstract = True
