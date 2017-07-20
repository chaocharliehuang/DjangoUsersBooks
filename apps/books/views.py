from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..users.models import *

def index(request):
    if 'id' not in request.session:
        return redirect('/')
    return render(request, 'books/index.html')

def add(request):
    if 'id' not in request.session:
        return redirect('/')
    if 'book_title' not in request.session:
        request.session['book_title'] = ''
    if 'author_name' not in request.session:
        request.session['author_name'] = ''
    if 'review' not in request.session:
        request.session['review'] = ''
    
    context = {'authors': []}
    books = Book.objects.all()
    for book in books:
        context['authors'].append(book.author_name)
    return render(request, 'books/add.html', context)

def process_book(request):
    pass