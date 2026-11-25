from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
import os

def contact(request):
    if request.method == 'POST':
        # Handle the form submission here
        book_id = request.POST['book_id']
        book = request.POST['book']
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST.get('user_id') or 0
        seller_id = request.POST['seller_id']
        seller_email = request.POST['seller_email']
        
        # Check if user has already made inquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(book_id=book_id, user_id=user_id, seller_id=seller_id)
            if has_contacted:
                messages.error(request, 'You have already made inquiry for this book.')
                return redirect('/books/'+ book_id)
        
        contact = Contact(book=book, book_id=book_id, name=name, email=email, message=message, user_id=user_id, seller_id=seller_id)
        contact.save()
        # Send Email Config
        # Email is optional: the inquiry is already saved, so a missing or
        # wrong SMTP setup must not crash the page.
        recipients = [e for e in [seller_email, os.environ.get('EMAIL_RECEIVER')] if e]
        try:
            send_mail(
                'KitabKart Inquiry',
                'There has been an inquiry for book listing ' + book + '. Sign into the admin panel for more info',
                os.environ.get('EMAIL_SENDER'),
                recipients,
                fail_silently=False
            )
        except Exception as exc:
            print(f'Inquiry saved, but email was not sent: {exc}')
        
        messages.success(request, 'Your request has been submitted to seller will get back to you soon')
        return redirect('/books/'+ book_id)
