import logging

from django_auditor.models import EntityAuditLog

LOG = logging.getLogger(__name__)


class AuditLogModelRegistry(object):

    def __init__(self, include_log_models, exclude_log_fields):
        self.include_log_models = include_log_models
        self.exclude_log_fields = exclude_log_fields

    def track_audit_logs_entries(self, instance, performed_by=None):
        entity_log_datas = []
        try:
            if instance.__class__.__name__ in self.include_log_models:
                fields = instance._meta.fields
                for field in fields:
                    entity_log_data = self.__create_log_object(instance, field, performed_by)
                    if entity_log_data:
                        entity_log_datas.append(entity_log_data)
        except Exception as ex:
            LOG.error(ex, exc_info=True)
            LOG.exception('Parsing data for audit log fails')
            entity_log_datas = []
        return entity_log_datas

    def __create_log_object(self, instance, field, performed_by):
        entity_log_data = None
        if field.attname not in self.exclude_log_fields:
            old_value, operation_type = AuditLogModelRegistry.__get_old_value(instance, field)
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
                entity_log_data = data
        return entity_log_data

    @staticmethod
    def __get_old_value(instance, field):
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
        return old_value, operation_type

    @staticmethod
    def create_logs(instance_objects):
        try:
            EntityAuditLog.objects.bulk_create([EntityAuditLog(**o) for o in instance_objects])
        except Exception as ex:
            LOG.error(ex, exc_info=True)
            LOG.exception('Creation of audit log failed')


audit_log = AuditLogModelRegistry
