from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

NOTIFICATION_TYPES = (
    ('follow', 'New Follower'),
    ('like', 'Post Like'),
    ('comment', 'New Comment'),
    ('mention', 'Mention'),
    ('system', 'System Notification'),
)


class Notification(models.Model):
    """Notification model for user notifications."""
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions',
        null=True,
        blank=True
    )
    verb = models.CharField(max_length=255)
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='system'
    )
    
    # Generic foreign key for the target object (post, comment, etc.)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', 'created_at']),
        ]

    def __str__(self):
        return f"{self.verb} - {self.recipient.username}"

    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save()

    @classmethod
    def create_notification(cls, recipient, actor, verb, notification_type, target=None):
        """Helper method to create a notification."""
        notification = cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            notification_type=notification_type,
        )
        
        if target:
            notification.content_type = ContentType.objects.get_for_model(target)
            notification.object_id = target.id
            notification.save()
        
        return notification
