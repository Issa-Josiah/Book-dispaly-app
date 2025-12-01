from django import forms
from .models import Book, Author, Category, BorrowRecord
from django.utils import timezone
from datetime import timedelta

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