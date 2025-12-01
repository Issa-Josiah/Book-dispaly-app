<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404, redirect
=======


from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
>>>>>>> 764b516a946b49efea48ce199513338a7f4040f0
from django.contrib import messages
from django.utils import timezone
from .models import Book, Author, Category, BorrowRecord
from .forms import BookForm, AuthorForm, CategoryForm, BorrowForm, ReturnForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator



# Dashboard view
@login_required
def dashboard(request):
<<<<<<< HEAD
    # Dashboard view that will show all the liblary statistics
=======
>>>>>>> 764b516a946b49efea48ce199513338a7f4040f0
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='available').count()
    borrowed_books = Book.objects.filter(status='borrowed').count()
    total_authors = Author.objects.count()
<<<<<<< HEAD
    total_categories = Category.objects.count()

    recent_activity = BorrowRecord.objects.order_by('-borrow_date')[:5]
    overdue_books = BorrowRecord.objects.filter(is_returned=False, due_date__lt=timezone.now())
    categories = Category.objects.all()

    context = {
=======
    recent_borrowed = BorrowRecord.objects.order_by('-borrow_date')[:5]

    context = {
        'title': 'Dashboard',
>>>>>>> 764b516a946b49efea48ce199513338a7f4040f0
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'total_authors': total_authors,
<<<<<<< HEAD
        'total_categories': total_categories,
        'recent_activity': recent_activity,
        'overdue_books': overdue_books,
        'categories': categories,}
    return render(request, 'book/dashboard.html', context)


# -----------------------------
# BOOK VIEWS
# -----------------------------
def book_list(request):
    search_query = request.GET.get('search', '')
    books = Book.objects.all()
    if search_query:
        books = books.filter(title__icontains=search_query)

    context = {
        'books': books,
        'request': request,
    }
    return render(request, 'book/book.html', context)

def book_create(request):
    form = BookForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'title': 'Add New'}
    if form.is_valid():
        form.save()
        messages.success(request, "Book created successfully.")
        return redirect('book:book_list')
    return render(request, 'book/book_form.html', context)

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, "Book updated successfully.")
        return redirect('book:book_list')
    return render(request, 'book/book_form.html', {'form': form, 'title': 'Edit'})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context =  {'book': book}
    return render(request, 'book/book_detail.html',context)

# -----------------------------
# AUTHOR VIEWS
# -----------------------------
def author_list(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'book/author_list.html', context)

def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Author created successfully.")
        return redirect('book:author_list')
    return render(request, 'book/author_form.html', {'form': form, 'title': 'Add Author'})

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST , instance=author)
    if form.is_valid():
        form.save()
        messages.success(request, "Author updated successfully.")
        return redirect('book:author_list')
    return render(request, 'book/author_form.html', {'form': form, 'title': 'Edit Author'})

# -----------------------------
# CATEGORY VIEWS
# -----------------------------
def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'book/category_list.html', context)

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category created successfully.")
        return redirect('book:category_list')
    return render(request, 'book/category_form.html', {'form': form, 'title': 'Add Category'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect('book:category_list')
    return render(request, 'book/category_form.html', {'form': form, 'title': 'Edit Category'})


# -----------------------------
# BORROW VIEWS
# -----------------------------
def borrow_list(request):
    available_books = Book.objects.filter(status='available')
    borrowed_records = BorrowRecord.objects.filter(is_returned=False)

    context = {
        'available_books': available_books,
        'borrowed_records': borrowed_records,
        'request': request,
    }
    return render(request, 'book/borrow_list.html', context)

def borrow_create(request):
    book_id = request.GET.get('book')
    initial = {}
    if book_id:
        initial['book'] = get_object_or_404(Book, pk=book_id)

    form = BorrowForm(request.POST or None, initial=initial)
    if form.is_valid():
        borrow = form.save(commit=False)
        borrow.save()
        borrow.book.status = 'borrowed'
        borrow.book.save()
        messages.success(request, "Book borrowed successfully.")
        return redirect('book:borrow_list')
    return render(request, 'book/borrow_form.html', {'form': form, 'title': 'Borrow Book'})

# -----------------------------
# RETURN VIEWS
# -----------------------------
def return_list(request):
    returned_records = BorrowRecord.objects.filter(is_returned=True).order_by('-return_date')
    unreturned_records = BorrowRecord.objects.filter(is_returned=False)
    currently_borrowed_count = BorrowRecord.objects.filter(is_returned=False).count()
    overdue_count = BorrowRecord.objects.filter(is_returned=False, due_date__lt=timezone.now()).count()
    returned_this_month = BorrowRecord.objects.filter(
        is_returned=True,
        return_date__month=timezone.now().month
    ).count()

    context = {
        'returned_records': returned_records,
        'unreturned_records': unreturned_records,
        'currently_borrowed_count': currently_borrowed_count,
        'overdue_count': overdue_count,
        'returned_this_month': returned_this_month,
    }
    return render(request, 'book/return_list.html', context)

def return_book(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk)
    if request.method == 'POST':
        record.is_returned = True
        record.return_date = timezone.now()
        record.save()
        record.book.status = 'available'
        record.book.save()
        messages.success(request, "Book returned successfully.")
        return redirect('book:return_list')
    return render(request, 'book/return_confirm.html', {'record': record})
=======
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
>>>>>>> 764b516a946b49efea48ce199513338a7f4040f0
