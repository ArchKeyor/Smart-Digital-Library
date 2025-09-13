from django.shortcuts import render
from .models import Book
from django.shortcuts import get_object_or_404, render
# Create your views here.
def book_list(request):
    books = Book.published.all()
    return render(
        request,
        'virtuallibrary/book/list.html',
        {'books': books}
    )
def book_detail(request,id):
    book = get_object_or_404(Book,id=id,status=Book.Status.PUBLISHED)
    return render(
        request,
        'virtuallibrary/book/detail.html',
        {'book':book}
    )