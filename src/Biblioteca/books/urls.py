from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import BookListView, BookDetailView


urlpatterns = [
    path('', login_required(BookListView.as_view()), name='book-list'),
    path('<slug:pk>/',
         login_required(BookDetailView.as_view()), name='book-detail'),
]
