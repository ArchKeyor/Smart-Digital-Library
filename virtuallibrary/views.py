from taggit.models import Tag
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from .models import Book, Emprestimo
from .forms import SearchForm
from django.conf import settings
from datetime import timedelta, date
from django.contrib import messages
from django.utils.text import slugify

def book_list(request, tag_slug=None):
    book_list = Book.published.all()
    tag = None
    search_form = SearchForm()
    query = None
    all_tags = Tag.objects.filter(taggit_taggeditem_items__content_type__model='book').distinct()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        book_list = book_list.filter(tags__in=[tag])

    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            book_list = book_list.filter(
                Q(title__icontains=query) | 
                Q(body__icontains=query) |
                Q(author__icontains=query)
            ).distinct()

    paginator = Paginator(book_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
        
    return render(
        request,
        'virtuallibrary/book/list.html',
        {
            'books': books,
            'tag': tag,
            'search_form': search_form,
            'query': query,
            'all_tags': all_tags,
        }
    )

def book_detail(request, id):
    book = get_object_or_404(Book, id=id, status=Book.Status.PUBLISHED)
    book_tags_ids = book.tags.values_list('id', flat=True)
    similar_books = Book.published.filter(tags__in=book_tags_ids).exclude(id=book.id)
    similar_books = similar_books.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    
    return render(
        request,
        'virtuallibrary/book/detail.html',
        {
            'book': book,
            'similar_books': similar_books
        }
    )

def login_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            message = 'Usuário ou senha inválidos'

    return render(request, 'login/login.html', {'message': message})

def home_view(request):
    emprestimos = []
    if request.user.is_authenticated:
        emprestimos = Emprestimo.objects.filter(user=request.user).select_related('book')
        
        # Adiciona a data de devolução para cada empréstimo
        for emprestimo in emprestimos:
            emprestimo.data_devolucao = emprestimo.data_emprestimo + timedelta(days=14)
    
    return render(request, 'home/home.html', {
        'user': request.user,
        'emprestimos': emprestimos
    })

def logout_view(request):
    logout(request)
    return redirect('/')

def emprestar_livro(request, book_id):
    if request.user.is_authenticated:
        if Emprestimo.objects.filter(user=request.user).count() >= 3:
            messages.error(request, "Você já tem 3 livros emprestados. Devolva um livro primeiro.")
            return redirect('virtuallibrary:book_detail', id=book_id)

        book = get_object_or_404(Book, id=book_id)
        emprestimo, created = Emprestimo.objects.get_or_create(
            user=request.user, 
            book=book
        )
        return redirect('virtuallibrary:home')
    else:
        return redirect('virtuallibrary:login')
    
def devolver_livro(request, emprestimo_id):
    if request.user.is_authenticated:
        emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, user=request.user)
        emprestimo.delete()
        messages.success(request, f"Livro '{emprestimo.book.title}' devolvido com sucesso!")
    return redirect('virtuallibrary:home')

def profile_view(request):
    # Redireciona para a home
    return redirect('virtuallibrary:home')

# Funções de verificação de grupos
def is_bibliotecario(user):
    return user.is_authenticated and user.groups.filter(name='Bibliotecário').exists()

def is_professor(user):
    return user.is_authenticated and user.groups.filter(name='Professor').exists()

# Views exclusivas para bibliotecários
@user_passes_test(is_bibliotecario)
def gerenciar_acervo(request):
    books = Book.objects.all().order_by('-created')
    paginator = Paginator(books, 10)  # 10 livros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'virtuallibrary/gerenciar_acervo.html', {
        'books': page_obj,
        'page_obj': page_obj
    })

@user_passes_test(is_bibliotecario)
def adicionar_livro(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        body = request.POST.get('body', '')
        publication_date = request.POST.get('publication_date')
        cover = request.FILES.get('cover')
        tags_input = request.POST.get('tags', '')
        
        # Criar o slug automaticamente
        slug = slugify(title)
        
        # Verificar se já existe um livro com esse slug
        counter = 1
        original_slug = slug
        while Book.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # Criar o livro
        book = Book.objects.create(
            title=title,
            slug=slug,
            author=author,
            body=body,
            publication_date=publication_date or date.today(),
            cover=cover,
            posted_by=request.user,
            status='PB'  # Published
        )
        
        # Processar tags
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tag_names:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    book.tags.add(tag)
        
        messages.success(request, f"Livro '{title}' adicionado com sucesso!")
        return redirect('virtuallibrary:gerenciar_acervo')
    
    return render(request, 'virtuallibrary/adicionar_livro.html')

@user_passes_test(is_bibliotecario)
def editar_livro(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.body = request.POST.get('body', '')
        tags_input = request.POST.get('tags', '')
        
        publication_date = request.POST.get('publication_date')
        if publication_date:
            book.publication_date = publication_date
            
        # Verificar se foi enviada uma nova capa
        new_cover = request.FILES.get('cover')
        if new_cover:
            book.cover = new_cover
            
        # Atualizar slug se o título mudou
        new_slug = slugify(book.title)
        if new_slug != book.slug:
            counter = 1
            original_slug = new_slug
            while Book.objects.filter(slug=new_slug).exclude(id=book.id).exists():
                new_slug = f"{original_slug}-{counter}"
                counter += 1
            book.slug = new_slug
        
        # Atualizar tags
        book.tags.clear()  # Remove todas as tags antigas
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tag_names:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    book.tags.add(tag)
        
        book.save()
        messages.success(request, f"Livro '{book.title}' atualizado com sucesso!")
        return redirect('virtuallibrary:gerenciar_acervo')
    
    # Para mostrar as tags atuais no formulário de edição
    current_tags = ', '.join([tag.name for tag in book.tags.all()])
    
    return render(request, 'virtuallibrary/editar_livro.html', {
        'book': book,
        'current_tags': current_tags
    })

@user_passes_test(is_bibliotecario) 
def deletar_livro(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    title = book.title
    book.delete()
    messages.success(request, f"Livro '{title}' removido com sucesso!")
    return redirect('virtuallibrary:gerenciar_acervo')