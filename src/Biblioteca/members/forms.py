from django.forms import ModelForm
from django import forms
from .models import Loan, Member, Book, User
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ValidationError


class LoanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update('hidden', '1')        

    class Meta:
        fields = ['member', 'book', 'user', 'due_date']


class LoanABookForm( forms.Form ):
    member = forms.IntegerField()
    book = forms.IntegerField()        
    due_date = forms.DateTimeField()
    utc_offset_minutes = forms.IntegerField()
      

    def get_form_options( self ):
        
        form_options = {}
        form_options['dict'] = {'member': {}, 'book': {} }
        form_options['list'] = {'member': [], 'book': [] }
        
        members = Member.objects.filter(status='A')
        for member in members:
            form_options['list']['member'].append( { 'id' : member.id, 'value' : member.name } )
            form_options['dict']['member'][member.id] = { 'id' : member.id , 'value' : member.name }             
        
        books = Book.objects.filter(status='A')
        for book in books:            
            form_options['list']['book'].append( { 'id' : book.id, 'value' : book.name } )
            form_options['dict']['book'][book.id] = { 'id' : book.id , 'value' : book.name }        

        return form_options
       

     
    def clean(self):
        cleaned_data = super().clean()
        
        utc_offset_minutes = cleaned_data.get('utc_offset_minutes')
 
        due_date = cleaned_data.get('due_date')       
        due_date = due_date + timedelta(minutes = utc_offset_minutes)

        now = datetime.now(timezone.utc)
        
        if due_date <= now:
            message = 'Due time must be after current time'
            self.add_error('due_date', message)

        if due_date == '':     
            message = 'Due time was not informated'
            self.add_error('due_date', message)
    
        return due_date

        
    def clean_book(self):
        data = self.cleaned_data["book"]
        
        try:
            book = Book.objects.get(pk = data)
        except Book.DoesNotExist:
            raise ValidationError('Book identification is not valid')
        
        if book.status != 'A':
            raise ValidationError('Book is not available')
        
        if data == '':
            raise ValidationError('Book identification was not provided')

        return data

    def clean_member(self):
        
        data = self.cleaned_data["member"]
        
        if data == "":
            raise ValidationError('Member identfication was not provided')
                
        try:
            member = Member.objects.get(pk = data)
        except Member.DoesNotExist:
            raise ValidationError('Member identification is not valid')
        
        if member.status != 'A':
            raise ValidationError('Member has no "Activo" status')
        
        return data

    
    def save(self, commit=True, authorized_user = None):

        field_values = {}
        for field in self:
            if field.value():
                field_values[field.html_name] = field.value()
        
        book_object = Book.objects.get( id=field_values['book'] )
        book_object.status = 'P'
        
        loan_object = Loan( 
                status = 'P',                
                user = authorized_user,
                member = Member.objects.get(id=field_values['member']),
                book = book_object,
                due_date= field_values['due_date'],
        )

        if commit:
            loan_object.save()
            book_object.save()
        
        return loan_object
    