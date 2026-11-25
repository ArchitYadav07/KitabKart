from .models import Book

# Dropdown choices for the search form, built from the books in the database.
# Values are de-duplicated and sorted.


def get_publication_choices():
    return sorted(set(Book.objects.filter(is_published=True).values_list('publication', flat=True)))


def get_published_year_choices():
    return sorted(set(Book.objects.filter(is_published=True).values_list('published_year', flat=True)), reverse=True)


def get_price_choices():
    return sorted(set(Book.objects.filter(is_published=True).values_list('price', flat=True)))
