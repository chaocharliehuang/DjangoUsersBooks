from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

# from .models import Book

def index(request):
    return render(request, 'books/index.html')