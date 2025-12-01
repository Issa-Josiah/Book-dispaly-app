from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    # dashboard
    path('start/', views.dashboard, name='dashboard'),

    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/edit/<int:pk>', views.book_update, name='book_update'),
    path('books/<int:pk>', views.book_detail, name='book_detail'),
    # Authors
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.author_create, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_update, name='author_update'),


    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    # Borrow Records
    path('borrow/', views.borrow_list, name='borrow_list'),
    path('borrow/add/', views.borrow_create, name='borrow_create'),
    # Return URLs
    path('return/', views.return_list, name='return_list'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
]


