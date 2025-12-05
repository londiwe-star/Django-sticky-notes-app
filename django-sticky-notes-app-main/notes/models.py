"""
Models for the notes app.
"""
from django.db import models


class NoteManager(models.Manager):
    """Custom manager for Note model."""
    
    def get_recent(self):
        """Return recently updated notes."""
        return self.get_queryset().order_by('-updated_at')


class Note(models.Model):
    """Model representing a sticky note."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NoteManager()

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

