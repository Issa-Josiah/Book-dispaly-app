from django import forms
from .models import Book, Author, Category, BorrowRecord
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class AuthorForm(forms.ModelForm):
    #form for creating and updating authors
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date']
        widgets = {
            'name': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter author biography'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'name': 'Author Name',
            'bio': 'Biography',
            'birth_date': 'Birth Date',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter category description'
            }),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Description',
        }

#book form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'author', 'category', 'description', 'published_date',  'pages', 'status', 'cover_image']#'publisher',
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN (optional)'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter book description'
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            # 'publisher': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Enter oublisher name'
            # }),
            'pages': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of pages'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Book Title',
            'isbn': 'ISBN',
            'author': 'Author',
            'category': 'Category',
            'description': 'Description',
            'published_date': 'Published Date',
            'publisher': 'Publisher',
            'pages': 'Number of Pages',
            'status': 'Status',
            'cover_image': 'Cover Image',
        }

class BorrowForm(forms.ModelForm):
    #form for borrowing books
    borrower = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Borrower'
    )

    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrower', 'due_date', 'notes']
        widgets = {
            'book': forms.Select(attrs={
                'class': 'form-select'
            }),
            'due_date': forms.Select(attrs={
                'class': 'form-control',
                'type': 'datetime-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes (optional)'
            }),
        }
        labels = {
            'book': 'Book',
            'borrower': 'Borrower',
            'due_date': 'Due Date',
            'notes': 'Notes',
        }

        #display/show available books
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['book'].queryset = Book.objects.filter(status='available')
            #we can set the due date to 14 days from now
            if not self.instance.pk:
                default_due = timezone.now() + timedelta(days=14)
                self.fields['due_date'].initial = default_due.strftime('%Y-%m-%dT%H:%M')

#form for returning books
class ReturnForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['return_date', 'notes']
        widgets = {
            'return_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Return notes (optional)'
            }),
        }
        labels = {
            'return_date': 'Return Date',
            'notes': 'Notes',
        }

        #set the return date as now
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            #set default time here
            if not self.instance.return_date:
                self.fields['return_date'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
                #%Y-%m-%d %H:%M:%S” represents the year, month, day, hour, minute, and second in a specific order