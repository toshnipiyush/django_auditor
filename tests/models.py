from django.db import models

from django_auditor.extensions import AuditLogBaseModel


class TestModel(AuditLogBaseModel):
    username = models.CharField(max_length=251)
    created_on = models.DateTimeField(verbose_name="Created On", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Updated On", auto_now_add=True)

    class Meta:
        db_table = "test_model"
        verbose_name = "Test Model"
        verbose_name_plural = "Test Model"

    def __str__(self):
        return self.username
