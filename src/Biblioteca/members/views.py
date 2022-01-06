
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import LoanForm
from .models import Member, Loan



class MemberListView(ListView):
    model = Member


class MemeberView(DetailView):
    model = Member


class LoanListView(ListView):
    model = Loan


class LoanView(DetailView):
    model = Loan
