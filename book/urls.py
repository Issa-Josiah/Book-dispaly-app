from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    # dashboard
    path('', views.dashboard, name='dashboard'),

    # Books

    # Authors

    # Categories

    # Borrow Records
]