
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import LoanForm
from .models import Member, Loan



class MemberListView(ListView):
    model = Member

    def get_queryset(self):
        queryset = Member.objects.all()
        name = self.request.GET.get('name','-')
        if name != '-':
            queryset = Member.objects.filter(
                name__icontains=name
                )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('name', '-')
        if name != '-':
            context['search_text'] = name
        return context


class MemeberView(DetailView):
    model = Member


class LoanListView(ListView):
    model = Loan


class LoanView(DetailView):
    model = Loan
