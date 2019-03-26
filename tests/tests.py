from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_auditor.models import EntityAuditLog
from tests.models import TestModel


class TestEditLogs(TestCase):
    def _assertEqualLogsCount(self, log_count, instance, operation_type, attribute=None):
        kwargs = {
            'fm_entity_type': ContentType.objects.get_for_model(instance),
            'fk_entity_id': instance.id,
            'operation_type': operation_type
        }
        if attribute:
            kwargs['attribute'] = attribute
        event_count = EntityAuditLog.objects.filter(**kwargs).count()
        self.assertEqual(event_count, log_count)

    def test_driver_create_logs(self):
        # Registering log for create
        user = TestModel.objects.create(username="test_user")
        self._assertEqualLogsCount(1, user, EntityAuditLog.CREATED)

        # Registering log for update
        user.username = "update_user"
        user.save()
        self._assertEqualLogsCount(1, user, EntityAuditLog.UPDATED)
