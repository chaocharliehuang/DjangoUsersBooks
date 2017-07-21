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
    if request.method == "POST":
        # FORM VALIDATION
        errors_book = Book.objects.book_validator(request)
        if len(errors_book):
            for tag, error in errors_book.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('books:add'))

        errors_review = Review.objects.review_validator(request)
        if len(errors_review):
            for tag, error in errors_review.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('books:add'))

        # GATHER INFO
        user_id = request.session['id']
        book_title = request.POST['book_title']
        if request.POST['author_name_list'] == 'custom':
            author_name = request.POST['author_name']
        else:
            author_name = request.POST['author_name_list']
        review = request.POST['review']
        rating = int(request.POST['rating'])

        # CHECK IF BOOK TITLE IS ALREADY IN DATABASE
        books = Book.objects.filter(title=book_title)
        if len(books) < 1:
            new_book = Book.objects.create(title=book_title, author_name=author_name)
        else:
            new_book = books.first()
        book_id = new_book.id

        # ADD BOOK AND REVIEW TO DATABASE
        curr_user = User.objects.get(id=user_id)
        curr_user.books.add(new_book)
        new_review = Review.objects.create(review=review, rating=rating, book=new_book, user=curr_user)
        
        request.session['book_title'] = ''
        request.session['author_name'] = ''
        request.session['review'] = ''
        return redirect(reverse('books:display_book', args=(book_id,)))
    else:
        return redirect(reverse('books:add'))

def display_book(request, id):
    book = Book.objects.get(id=id)
    context = {
        'book_id': int(id),
        'book_title': book.title,
        'author_name': book.author_name,
        'reviews': []
    }
    reviews = Review.objects.filter(book__id=id).order_by('-created_at')
    for review in reviews:
        data = {
            'rating': review.rating * '*',
            'user': review.user.first_name,
            'user_id': review.user.id,
            'review': review.review,
            'review_id': review.id,
            'posted': review.created_at.strftime('%B %d, %Y')
        }
        context['reviews'].append(data)

    return render(request, 'books/book.html', context)

def delete_review(request, id):
    review = Review.objects.get(id=id)
    book_id = review.book.id
    review.delete()
    return redirect(reverse('books:display_book', args=(book_id,)))