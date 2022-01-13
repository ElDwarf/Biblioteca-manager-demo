from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Book


class BookListView(ListView):
    model = Book

    def get_queryset(self):
        queryset = Book.objects.all()
        name = self.request.GET.get('name', '-')
        if name != '-':
            queryset = Book.objects.filter(
                name__icontains=name
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('name', '-')
        if name != '-':
            context['search_text'] = name
        return context


class BookDetailView(DetailView):
    model = Book
