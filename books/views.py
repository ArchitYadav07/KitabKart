from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import get_price_choices, get_publication_choices, get_published_year_choices
from .models import Book


def books(request):
    books = Book.objects.order_by('-listing_date').filter(is_published=True)
    paginator = Paginator(books, 3)
    page = request.GET.get('page')
    paged_books = paginator.get_page(page)
    
    context = {
        'books': paged_books
    }
    return render(request, 'books/books.html', context)

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book
    }
    return render(request, 'books/book.html', context)

def search(request):
    queryset_list = Book.objects.order_by('-listing_date').filter(is_published=True)
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                Q(title__icontains=keywords) | Q(description__icontains=keywords)
            )
    if 'author' in request.GET:
        author = request.GET['author']
        if author:
            queryset_list = queryset_list.filter(author__icontains=author)
    if 'publication' in request.GET:
        publication = request.GET['publication']
        if publication:
            queryset_list = queryset_list.filter(publication__iexact=publication)
    if 'published_year' in request.GET:
        published_year = request.GET['published_year']
        if published_year:
            queryset_list = queryset_list.filter(published_year=published_year)
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
    context = {
        'publication_choices': get_publication_choices,
        'published_year_choices': get_published_year_choices,
        'price_choices': get_price_choices,
        'books': queryset_list,
        'values': request.GET
    }
    return render(request, 'books/search.html', context)
