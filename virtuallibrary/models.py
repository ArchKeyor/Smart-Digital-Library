from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

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
    
    # AUTOR REAL DO LIVRO (não o usuário do sistema)
    author = models.CharField(max_length=200, help_text="Nome do autor do livro", default="Autor Desconhecido")
    
    # DATA REAL DE PUBLICAÇÃO DO LIVRO (não quando foi postado no site)
    publication_date = models.DateField(help_text="Data original de publicação do livro", default="2024-01-01")
    
    # USUÁRIO QUE POSTOU NO SISTEMA
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books_posted',
        help_text="Admin que adicionou este livro ao sistema",
        default=1  # Assume que o primeiro usuário (ID=1) é o admin principal
    )
    
    # campo de capa
    cover = models.ImageField(
        upload_to='book_covers/',  # pasta dentro de MEDIA_ROOT
        blank=True,
        null=True
    )

    # DATA EM QUE FOI POSTADO NO SISTEMA
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # Corrigido: era auto_now_add
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
        return f"{self.title} - {self.author}"
    
    def get_absolute_url(self):
        return reverse(
            'virtuallibrary:book_detail', args=[self.id]
        )
class UserProfile(models.Model):
    TIPOS = [
        ('estudante', 'Estudante'),
        ('bibliotecario', 'Bibliotecário'),
        ('professor', 'Professor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_perfil = models.CharField(max_length=20, choices=TIPOS, default='estudante')
    data_nascimento = models.DateField(null=True, blank=True)
    matricula = models.CharField(max_length=20, blank=True)
    curso = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_perfil_display()}"