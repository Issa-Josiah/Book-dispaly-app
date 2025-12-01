from django.contrib import admin
from .models import Book, Author, Category, BorrowRecord


# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_date', 'created_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'isbn', 'author__name')
    ordering = ('title',)

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'borrow_date', 'due_date', 'is_returned')
    list_filter = ('is_returned',)
    search_fields = ('book__title', 'borrower__username')
    ordering = ('-borrow_date',)

