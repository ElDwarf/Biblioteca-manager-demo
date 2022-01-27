import pytest
from django.urls import reverse
import uuid
from .models import Member
from  books.models import Book, Author, Genre
from .views import LoanViews
from datetime import datetime, timedelta


@pytest.fixture
def test_password():
   return 'a-strong-test-pass'

@pytest.fixture
def authors(db):      
   author_objects = []   
   authors_data = [ 
         { 'name': 'author A'}, {'name': 'author B'},{ 'name': 'author C'} 
   ]
   for author_data in authors_data:        
      author_objects.append( Author.objects.create(**author_data ) )
   return author_objects


@pytest.fixture
def genres(db):      
   genre_objects = []   
   genres_data = [ 
         { 'name': 'genre A'}, {'name': 'genre B'},{ 'name': 'genre C'} 
   ]
   for genre_data in genres_data:        
      genre_objects.append( Genre.objects.create(**genre_data ) )
   return genre_objects

@pytest.fixture
def books(db, authors, genres):      
   book_objects = []
   now = datetime.now()   
   now_minus_3_hours = now - timedelta(minutes = 180)    
   books_data = [ 
         { 
         'name': 'Book A',
         'genre': genres[0],
         'author': authors[0],
         'status': 'A',
         'printed_date': now_minus_3_hours,},
          { 
         'name': 'Book B',
         'genre': genres[1],
         'author': authors[1],
         'status': 'B',
         'printed_date': now_minus_3_hours,},
          { 
         'name': 'Book C',
         'genre': genres[0],
         'author': authors[2],
         'status': 'A',
         'printed_date': now_minus_3_hours,}, 
         { 
         'name': 'Book D',
         'genre': genres[0],
         'author': authors[1],
         'status': 'A',
         'printed_date': now_minus_3_hours,},
         { 
         'name': 'Book E',
         'genre': genres[1],
         'author': authors[2],
         'status': 'A',
         'printed_date': now_minus_3_hours,}  
   ]
   for book_data in books_data:        
      book_objects.append( Book.objects.create(**book_data ) )
   return book_objects


@pytest.fixture
def members(db):      
   member_objects = []   
   members_data = [ 
         { 
         'name': 'Member A',
         'email': 'testa@test.com',         
         'status': 'A'},
         { 
         'name': 'Member B',
         'email': 'testb@test.com',         
         'status': 'A'},
         { 
         'name': 'Member C',
         'email': 'testc@test.com',         
         'status': 'B'}
   ]
   for member_data in members_data:        
      member_objects.append( Member.objects.create(**member_data ) )
   return member_objects


@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user

#def test_answer():
   #assert LoanViews.my_test_funct(3) == 4

@pytest.mark.django_db
def test_logged_out_loan_a_book_view(client):
   url = reverse('loan_a_book')
   response = client.get(url)      
   #redirection 302 due @login_required
   assert response.status_code == 302

@pytest.mark.django_db
def test_no_members_nor_books_loan_a_book_view(client, create_user, test_password):
   user = create_user()
   client.login(username=user.username, password=test_password)
   url = reverse('loan_a_book')
   response = client.get(url)         
   assert response.status_code == 202

@pytest.mark.django_db
def test_login_view(client):
   url = reverse('login')
   response = client.get(url)      
   assert response.status_code == 200


@pytest.mark.django_db
def test_no_available_members_loan_a_book_view(client, create_user, test_password, books):
   user = create_user()   
   client.login(username=user.username, password=test_password )   
   url = reverse('loan_a_book')
   response = client.get(url)
   assert response.status_code == 202

@pytest.mark.django_db
def test_no_availabe_books_loan_a_book_view(client, create_user, test_password, members):
   user = create_user()   
   client.login(username=user.username, password=test_password )         
   url = reverse('loan_a_book')
   response = client.get(url)
   assert response.status_code == 202


@pytest.mark.django_db
def test_successfull_loan_a_book_view(client, create_user, books, members, test_password):   
   user = create_user()
   client.login( username=user.username, password=test_password )
   url = reverse('loan_a_book')
   now = datetime.now()   
   utc_offset_minutes = 180   
   due_date = now + timedelta( minutes = utc_offset_minutes + 3)
   due_date.strftime('%Y-%m-%dT%H:%M')     
   
   loans_data = [
      {            
      'book': books[0].id,            
      'member': members[1].id,
      'due_date': due_date,      
      'utc_offset_minutes': utc_offset_minutes },
      {            
      'book': books[2].id,            
      'member': members[0].id,
      'due_date': due_date,      
      'utc_offset_minutes': utc_offset_minutes },
      {            
      'book': books[3].id,            
      'member': members[1].id,
      'due_date': due_date,      
      'utc_offset_minutes': utc_offset_minutes },
      {            
      'book': books[4].id,            
      'member': members[1].id,
      'due_date': due_date,         
      'utc_offset_minutes': utc_offset_minutes }
   ]

   for loan_data in loans_data:
      response = client.post(url, loan_data)
      if response.status_code != 201: break
   
   assert response.status_code == 201



@pytest.mark.django_db
def test_not_valid_data_loan_a_book_view(client, create_user, books, members, test_password):   
   user = create_user()
   client.login( username=user.username, password=test_password  )
   url = reverse('loan_a_book')
   now = datetime.now()   
   utc_offset_minutes = 180   
   
   not_valid_due_date = now + timedelta( minutes = utc_offset_minutes - 360)
   not_valid_due_date.strftime('%Y-%m-%dT%H:%M')               

   valid_due_date = now + timedelta( minutes = utc_offset_minutes )
   valid_due_date.strftime('%Y-%m-%dT%H:%M')               
   
   loans_data = [
      {            
      'book': books[0].id,            
      'member': members[1].id,
      'due_date': not_valid_due_date,      
      'utc_offset_minutes': utc_offset_minutes },
      {            
      'book': books[1].id,            
      'member': members[0].id,
      'due_date': valid_due_date,      
      'utc_offset_minutes': utc_offset_minutes },
      {            
      'book': books[2].id,            
      'member': members[1].id,
      'due_date': not_valid_due_date,      
      'utc_offset_minutes': utc_offset_minutes },
      {            
      'book': books[0].id,            
      'member': members[2].id,
      'due_date': valid_due_date,         
      'utc_offset_minutes': utc_offset_minutes }
   ]

   for loan_data in loans_data:
      response = client.post(url, loan_data)
      if response.status_code != 400: break
   
   assert response.status_code == 400

