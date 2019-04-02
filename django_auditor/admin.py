from django.contrib import admin
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.core.exceptions import PermissionDenied

from django_auditor.models import EntityAuditLog


class EntityAuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'fm_entity_type', 'fk_entity_id', 'attribute', 'attribute_type', 'old_value', 'new_value',
                    'performed_by', 'operation_type', 'recorded_on', 'created_on', 'comments',)
    search_fields = ('id', 'attribute', 'old_value', 'new_value', 'performed_by__username',)
    list_filter = ('operation_type', 'fm_entity_type', 'attribute_type',)

    class Meta:
        model = EntityAuditLog

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class DjangoAuditorAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        if not self.has_delete_permission(request):
            raise PermissionDenied
        if request.POST.get('post'):
            for obj in queryset:
                obj.delete()
        else:
            return delete_selected_(self, request, queryset)


admin.site.register(EntityAuditLog, EntityAuditLogAdmin)
