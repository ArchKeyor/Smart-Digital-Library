from taggit.models import Tag
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from .models import Book
from .forms import SearchForm, SimpleAuthForm

def book_list(request, tag_slug=None):
    book_list = Book.published.all()
    tag = None
    search_form = SearchForm()
    query = None

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
                Q(author__username__icontains=query)
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
            'query': query
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

def simple_auth(request):
    message = ""
    
    if request.method == 'POST':
        form = SimpleAuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Tenta fazer login primeiro
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('virtuallibrary:book_list')
            else:
                # Se não conseguir login, cria usuário novo
                if User.objects.filter(username=username).exists():
                    message = "Usuário existe mas senha está errada"
                else:
                    # Criar usuário novo
                    user = User.objects.create_user(username=username, password=password)
                    login(request, user)
                    return redirect('virtuallibrary:book_list')
    else:
        form = SimpleAuthForm()
    
    return render(request, 'virtuallibrary/login.html', {'form': form, 'message': message})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('virtuallibrary:book_list')