from taggit.models import Tag
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from .models import Book
from django.db.models import Count

def book_list(request,tag_slug=None):
    book_list = Book.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        book_list = book_list.filter(tags_in=[tag])

    paginator = Paginator(book_list,3)
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
        {'books': books,
         'tag': tag}
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