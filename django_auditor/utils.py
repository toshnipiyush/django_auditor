import logging

from django_auditor.constants import INCLUDE_AUDIT_LOG_MODEL, EXCLUDE_AUDIT_LOG_FIELDS
from django_auditor.models import EntityAuditLog

LOG = logging.getLogger(__name__)


def track_audit_logs_entries(instance, performed_by=None):
    entity_log_data = []
    try:
        if instance.__class__.__name__ in INCLUDE_AUDIT_LOG_MODEL:
            fields = instance._meta.fields
            for field in fields:
                if field.attname not in EXCLUDE_AUDIT_LOG_FIELDS:
                    if instance.pk is None:
                        operation_type = EntityAuditLog.CREATED
                        old_value = None

                    else:
                        operation_type = EntityAuditLog.UPDATED
                        old_value = getattr(type(instance).objects.filter(pk=instance.pk).first(), field.name)
                        if field.choices:
                            for choice, identifier in field.choices:
                                if str(choice) == old_value:
                                    old_value = identifier
                    new_value = getattr(instance, "get_{}_display".format(field.name))() if field.choices else getattr(
                        instance, field.name, None)

                    if old_value != new_value:
                        data = {
                            'operation_type': operation_type,
                            'attribute': field.name,
                            'target': instance,
                            'performed_by_id': performed_by,
                            'comments': None,
                            'old_value': old_value,
                            'new_value': new_value
                        }
                        entity_log_data.append(data)
    except Exception as ex:
        LOG.error(ex, exc_info=True)
        LOG.exception('Parsing data for audit log fails')
        entity_log_data = []
    return entity_log_data


def create_logs(logs):
    log_instances = []
    try:
        for log in logs:
            log_instances.append(EntityAuditLog(**log))
        if log_instances:
            EntityAuditLog.objects.bulk_create(log_instances)
    except Exception as ex:
        LOG.error(ex, exc_info=True)
        LOG.exception('Creation of audit log failed')
