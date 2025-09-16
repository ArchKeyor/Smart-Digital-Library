from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
 def get_queryset(self):
     return (super().get_queryset().filter(status=Book.Status.PUBLISHED))
 
class Book(models.Model):
    tags = TaggableManager()
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
        # campo de capa
    cover = models.ImageField(
        upload_to='book_covers/',  # pasta dentro de MEDIA_ROOT
        blank=True,
        null=True
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
    def get_absolute_url(self):
        return reverse(
            'virtuallibrary:book_detail', args=[self.id]
        )