from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Borrow

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.available:
        Borrow.objects.create(book=book, user=request.user)
        book.available = False
        book.save()
    return redirect('book_list')

@login_required
def return_book(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id)
    borrow.returned_at = timezone.now()
    borrow.book.available = True
    borrow.book.save()
    borrow.save()
    return redirect('borrow_list')

@login_required
def borrow_list(request):
    borrows = Borrow.objects.filter(user=request.user)
    return render(request, 'library/borrow_list.html', {'borrows': borrows})
