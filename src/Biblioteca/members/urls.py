from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import MemberListView, MemeberView, LoanListView, LoanView

from . import views


urlpatterns = [
    path('', login_required(MemberListView.as_view()), name='member-list'),
    path('<int:pk>/',
         login_required(MemeberView.as_view()), name='member-detail'),
    path('loans', login_required(LoanListView.as_view()), name='loan-list'),
    path('loans/<int:pk>/', login_required(LoanView.as_view()), name='loan-list'),    
    
    path('loan-a-book/', views.LoanViews.loan_a_book, name='loan_a_book'),
]

