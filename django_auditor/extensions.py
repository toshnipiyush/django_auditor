from datetime import datetime

from django.db import models

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
        timestamp = datetime.now()
        entity_logs = audit_log(self.include_log_models, self.exclude_log_fields)\
            .track_audit_logs_entries(self, timestamp)
        super_data = super(AuditLogBaseModel, self).save(*args, **kwargs)
        audit_log.create_logs(entity_logs)
        return super_data

    def delete(self, using=None, keep_parents=False):
        timestamp = datetime.now()
        entity_logs = audit_log(self.include_log_models, self.exclude_log_fields) \
            .track_audit_logs_entries(self, timestamp, is_delete=True)
        audit_log.create_logs(entity_logs)
        return super(AuditLogBaseModel, self).delete()

    class Meta:
        abstract = True
