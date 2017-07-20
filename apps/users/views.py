from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

import bcrypt

# from .models import User

def index(request):
    return render(request, 'users/index.html')