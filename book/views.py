

from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib import messages
from .models import Book, Author, Category, BorrowRecord
from .forms import BookForm, AuthorForm, CategoryForm, BorrowForm, ReturnForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator



# Dashboard view
@login_required
def dashboard(request):
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='available').count()
    borrowed_books = Book.objects.filter(status='borrowed').count()
    total_authors = Author.objects.count()
    recent_borrowed = BorrowRecord.objects.order_by('-borrow_date')[:5]

    context = {
        'title': 'Dashboard',
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'total_authors': total_authors,
        'recent_borrowed': recent_borrowed,
    }
    return render(request, 'book/dashboard.html', context)


# ------------------ Book Views ------------------
@login_required

def book_list(request):
    books = get_list_or_404(Book.objects.all())  # List view using get_list_or_404
    return render(request, 'book/book_list.html', {'books': books, 'title': 'Books'})

@login_required
def available_books(request):
    book = get_list_or_404(Book.objects.all())
    return render(request, 'book/available_books.html', {'available_books':book, 'title': 'Available Books' })



@login_required

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Single book

    return render(request, 'book/base.html', {'book': book, 'title': book.title})


@login_required

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('book:book_list')
    else:
        form = BookForm()
    return render(request, 'book/book_form.html', {'form': form, 'title': 'Add Book'})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('book:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book/book_form.html', {'form': form, 'title': 'Edit Book'})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect('book:book_list')
    return render(request, 'book/book_confirm_delete.html', {'book': book, 'title': 'Delete Book'})


# ------------------ Author Views ------------------
@login_required
def author_list(request):
    authors = get_list_or_404(Author.objects.all())
    return render(request, 'book/author_list.html', {'authors': authors, 'title': 'Authors'})


@login_required
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'book/author_detail.html', {'author': author, 'title': author.name})


# ------------------ Category Views ------------------
@login_required
def category_list(request):
    categories = get_list_or_404(Category.objects.all())
    return render(request, 'book/category_list.html', {'categories': categories, 'title': 'Categories'})


@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'book/category_detail.html', {'category': category, 'title': category.name})


# ------------------ Borrow Views ------------------
@login_required
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow_record = form.save(commit=False)
            borrow_record.book.status = 'borrowed'
            borrow_record.book.save()
            borrow_record.save()
            messages.success(request, "Book borrowed successfully!")
            return redirect('book:dashboard')
    else:
        form = BorrowForm()
    return render(request, 'book/borrow_form.html', {'form': form, 'title': 'Borrow Book'})


@login_required
def return_book(request, pk):
    borrow_record = get_object_or_404(BorrowRecord, pk=pk)
    if request.method == 'POST':
        form = ReturnForm(request.POST, instance=borrow_record)
        if form.is_valid():
            borrow_record = form.save(commit=False)
            borrow_record.is_returned = True
            borrow_record.book.status = 'available'
            borrow_record.book.save()
            borrow_record.save()
            messages.success(request, "Book returned successfully!")
            return redirect('book:dashboard')
    else:
        form = ReturnForm(instance=borrow_record)
    return render(request, 'book/return_form.html', {'for