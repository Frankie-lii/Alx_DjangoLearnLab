from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_view", "Can view book details"),
            ("can_create", "Can create new book"),
            ("can_edit", "Can edit existing book"),
            ("can_delete", "Can delete book"),
        ]

# ✅ Notes:
# 1. Permissions above are custom-defined in the Meta class.
# 2. They’ll automatically appear in Django Admin after migrations.
# 3. You can then assign these permissions to groups (Editors, Viewers, Admins).

