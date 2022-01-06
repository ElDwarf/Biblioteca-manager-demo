from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Book


class BookListView(ListView):

    model = Book


class BookDetailView(DetailView):
    model = Book
