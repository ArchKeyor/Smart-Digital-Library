from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Book.Status.PUBLISHED)


class Book(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    author = models.CharField(max_length=200, help_text="Nome do autor do livro", default="Autor Desconhecido")
    publication_date = models.DateField(help_text="Data original de publicação do livro", null=True, blank=True)
    
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books_posted',
        help_text="Admin que adicionou este livro ao sistema"
    )
    
    cover = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )
    
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    tags = TaggableManager()
    
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def get_absolute_url(self):
        return reverse('virtuallibrary:book_detail', args=[self.id])


class UserProfile(models.Model):
    TIPOS = [
        ('estudante', 'Estudante'),
        ('bibliotecario', 'Bibliotecário'),
        ('professor', 'Professor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_perfil = models.CharField(max_length=20, choices=TIPOS, default='estudante')
    primeiro_nome = models.CharField(max_length=50, blank=True, null=True)
    ultimo_nome = models.CharField(max_length=50, blank=True, null=True)
    curso = models.TextField(max_length=100,blank=True,null=True)
    matricula = models.CharField(max_length=30,blank=True,null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.tipo_perfil}"

class Emprestimo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-data_emprestimo']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"