
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpRequest
from .models import Member, Loan
from .forms import LoanABookForm
from django.contrib.auth.decorators import login_required


class MemberListView(ListView):
    model = Member


class MemeberView(DetailView):
    model = Member


class LoanListView(ListView):
    model = Loan


class LoanView(DetailView):
    model = Loan


class LoanViews():

    @login_required
    #@permission_required('loan.add')
    #@permission_required('book.update')
    def loan_a_book( request ):
                
        form_validation_message = {}
        form_values = {}
        status_code = None
                
        if request.method == 'POST':
            form = LoanABookForm(request.POST)
            if form.is_valid():                
                form_validation_message['title'] = {'type': 'success', 'text': 'Loan successfully registered'}                
                form.save( authorized_user=request.user )                
                status_code = 201
                form = LoanABookForm()
            else:
                form_validation_message['title'] = {'type': 'danger', 'text': 'Please correct this errors'}
                status_code = 400
                
        elif request.method == 'GET':
            form_validation_message['title'] = {'type': 'empty', 'text': ''}
            form_validation_message['secondary-title'] = {'type': 'empty', 'text': ''}
            form = LoanABookForm()            
        
        form_options = form.get_form_options()
        
        if form_options['dict']['book'] and form_options['dict']['member']:            
            if not status_code: status_code = 200
            for field in form:
                error_messages = [] 
                for message in field.errors:
                    error_messages.append(message )
                if not error_messages:
                    error_messages = ['']                
                form_validation_message[field.html_name] = error_messages
                
                field_value = field.value()
                
                if field.html_name in form_options['dict']:                    
                    first_index = next(iter(form_options['dict'][field.html_name])) 
                    form_values[field.html_name] = form_options['dict'][field.html_name][first_index]          
                else:
                    form_values[field.html_name] = {'id': 0, 'value': '' }
                
                if field_value:
                    if field.html_name in form_options['dict']:
                        if type( int(field_value) ) == int:
                            if int(field_value) in form_options['dict'][field.html_name]:                         
                                form_values[field.html_name] = form_options['dict'][field.html_name][int(field_value)]
                    else:
                        form_values[field.html_name] = {'id': 0, 'value': field_value }
        else:            
            validation_message = ''
            if not status_code: status_code = 202
            if not form_options['dict']['member']:
                validation_message = ' There are not available members to make a loan.'                
            if not form_options['dict']['book']:
                validation_message += ' There are not more available books to loan.'                
            form_validation_message['secondary_title'] = {'type': 'warning', 'text': validation_message}

        
        return render( request, 'loan_a_book.html',        
                {'form_validation_message': form_validation_message,
                 'form_values':form_values,
                 'form_options':form_options['list']
                 },
                 status = status_code,
        )

