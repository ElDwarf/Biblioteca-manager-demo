from django.db import models
from django.contrib.auth.models import User

from books.models import Book

from .status_choices import MEMBER_STATUS_CHOICES, LOAN_STATUS_CHOICES

class Member(models.Model):    
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=2, default='A', choices=MEMBER_STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, default='P', choices=LOAN_STATUS_CHOICES)
    due_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'El libro "{self.book}" prestado a "{self.member}"'
