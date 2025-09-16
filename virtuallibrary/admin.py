from django.contrib import admin
from .models import Book

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publication_date', 'posted_by', 'publish', 'status', 'cover']
    list_filter = ['status', 'created', 'publish', 'posted_by']  # Mudou 'author' para 'posted_by'
    search_fields = ['title', 'body', 'author']  # Agora 'author' é texto, pode buscar normalmente
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['posted_by']  # Mudou 'author' para 'posted_by' (que é ForeignKey)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facet = admin.ShowFacets.ALWAYS
    
    # Campos organizados em seções para facilitar o uso
    fieldsets = (
        ('Informações do Livro', {
            'fields': ('title', 'slug', 'author', 'publication_date', 'body', 'cover', 'tags')
        }),
        ('Configurações do Sistema', {
            'fields': ('posted_by', 'status', 'publish'),
            'classes': ('collapse',)  # Seção recolhível
        }),
    )
    