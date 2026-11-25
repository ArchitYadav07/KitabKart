"""Export books, sellers and contacts to data.json.

Usage:  python manage.py shell < export_json.py
"""
from itertools import chain

from django.core import serializers
from books.models import Book
from contacts.models import Contact
from sellers.models import Seller

objects = chain(Seller.objects.all(), Book.objects.all(), Contact.objects.all())
data = serializers.serialize("json", objects, indent=2)

with open("data.json", "w", encoding="utf-8") as out:
    out.write(data)

print("Exported to data.json")
