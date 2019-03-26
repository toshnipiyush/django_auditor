from django.db import models

from django_auditor.middleware import current_request
from django_auditor.registry import audit_log


class AuditLogBaseModel(models.Model):
    include_log_models = ['TestModel']
    exclude_log_fields = ['id', 'created_on', 'updated_on']

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        # ToDo: Log entries on delete operation
        request = current_request()
        performed_by = request.user.id if request else None
        entity_logs = audit_log(self.include_log_models, self.exclude_log_fields)\
            .track_audit_logs_entries(self, performed_by=performed_by)
        super_data = super(AuditLogBaseModel, self).save(*args, **kwargs)
        audit_log.create_logs(entity_logs)
        return super_data

    class Meta:
        abstract = True
