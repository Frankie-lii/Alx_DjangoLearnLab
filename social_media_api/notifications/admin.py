from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'actor', 'verb', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('recipient', 'actor', 'verb', 'notification_type')
        }),
        ('Target Object', {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
