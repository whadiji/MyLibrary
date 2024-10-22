from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Borrow
from django.core.paginator import Paginator
from .utils import formater_titre 
from .form import BookForm

def book_list(request):
    query = request.GET.get('q')  # Retrieve search parameter
    print("Requête de recherche : ", query)
    if query:
        books = Book.objects.filter(title__icontains=query)  # Filter books by title
    else:
        books = Book.objects.all()  # if you don't have filter => ALL  books

    for book in books:
        book.title = formater_titre(book.title)
      # Pagination
    paginator = Paginator(books, 3)  # 6 livres par page
    page_number = request.GET.get('page')  # Récupérer le numéro de page
    page_obj = paginator.get_page(page_number)  # Obtenir les livres de la page demandée

    return render(request, 'library/book_list.html', {'page_obj': page_obj, 'query': query})



@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.available:
        Borrow.objects.create(book=book, user=request.user)
        book.available = False
        book.save()
    return redirect('book_list')
def book_detail(request, book_id):
    # get a specific book with ID
    book = Book.objects.get(id=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

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

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  
    else:
        form = BookForm()


    return render(request, 'library/add_book.html', {'form': form})
