from django.shortcuts import render, get_list_or_404, redirect
from django.contrib import messages
from .models import Book, Author, Category, BorrowRecord
from .forms import BookForm, AuthorForm, CategoryForm, BorrowForm, ReturnForm


# Create your views here.


def dashboard(request):
    # Dashboard view that will show all the liblary statistics
    return render(request, 'book/dashboard.html')