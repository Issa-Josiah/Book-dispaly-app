from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    # dashboard
    path('d/', views.dashboard, name='dashboard'),

    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    # Authors
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),


    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    # Borrow Records
 path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
]

