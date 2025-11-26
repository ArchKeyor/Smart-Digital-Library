from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Book, UserProfile, Emprestimo

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
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil do usuário"

# Re-registrar o User já com o inline
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Primeiro remove o User padrão
admin.site.unregister(User)
# Agora registra o novo com o inline
admin.site.register(User, UserAdmin)

# Se quiser também pode registrar separado
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
        list_display = (
        "user", 
        "tipo_perfil", 
        "primeiro_nome", 
        "ultimo_nome",
        "curso",          
        "matricula",      
        "data_nascimento" 
    )
    
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'data_emprestimo', 'data_devolucao')
    list_filter = ('status',)
    search_fields = ('book__title', 'user__username')