from django.contrib import admin

from django_auditor.models import EntityAuditLog


class EntityAuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'fm_entity_type', 'fk_entity_id', 'attribute', 'old_value', 'new_value', 'performed_by',
                    'operation_type', 'created_on', 'comments',)
    search_fields = ('id', 'attribute', 'old_value', 'new_value', 'performed_by__phone_number',)
    list_filter = ('operation_type', 'fm_entity_type',)

    class Meta:
        model = EntityAuditLog

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(EntityAuditLog, EntityAuditLogAdmin)
