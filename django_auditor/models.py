from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE


class EntityAuditLog(models.Model):
    CREATED = 'CREATED'
    UPDATED = 'UPDATED'
    DELETED = 'DELETED'
    OPERATION_CHOICES = (
        (CREATED, 'CREATED'),
        (UPDATED, 'UPDATED'),
        (DELETED, 'DELETED')
    )

    operation_type = models.CharField(max_length=251, choices=OPERATION_CHOICES, verbose_name="Operation Type")
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, db_column="fk_performed_by_id",
                                     verbose_name="Operation Performed By", on_delete=CASCADE)
    fm_entity_type = models.ForeignKey(to=ContentType, db_column="fm_entity_id", verbose_name="Entity Type",
                                       on_delete=CASCADE)
    fk_entity_id = models.PositiveIntegerField(db_column="fk_entity_id", verbose_name="Entity ID")
    attribute = models.CharField(max_length=251, verbose_name="Field Name")
    old_value = models.CharField(max_length=251, db_column="old_value", verbose_name="Old Value", null=True, blank=True)
    new_value = models.CharField(max_length=251, db_column="new_value", verbose_name="New Value", null=True, blank=True)
    comments = models.CharField(max_length=1019, db_column="comments",
                                verbose_name="Comments", null=True, blank=True)
    created_on = models.DateTimeField(verbose_name="Created On", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated On", auto_now_add=True)
    target = GenericForeignKey("fm_entity_type", "fk_entity_id")

    class Meta:
        db_table = "entity_audit_log"
        verbose_name = "Entity Audit Log"
        verbose_name_plural = "Entity Audit Logs"

    def __str__(self):
        return "{} - {}".format(self.fm_entity_type, self.target)
