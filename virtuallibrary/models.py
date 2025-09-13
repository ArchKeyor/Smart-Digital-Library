from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class PublishedManager(models.Manager):
 def get_queryset(self):
     return (super().get_queryset().filter(status=Book.Status.PUBLISHED))
class Book(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='book_written',

    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2,
        choices = Status,
        default=Status.DRAFT    
    )
    objects = models.Manager()
    published = PublishedManager()
class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        def __str__(self):
            return self.title