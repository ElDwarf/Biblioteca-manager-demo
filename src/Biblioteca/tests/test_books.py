import uuid

import pytest

from django.urls import reverse
from django.contrib.auth.models import User


@pytest.fixture
def test_password():
   return 'strong-test-pass'

  
@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user


@pytest.mark.django_db
def test_view(client):
   url = reverse('book-list')
   response = client.get(url)
   assert response.status_code == 302


@pytest.mark.django_db
def test_auth_view(client, create_user, test_password):
   user = create_user()
   url = reverse('book-list')
   client.login(
       username=user.username, password=test_password
   )
   response = client.get(url)
   assert response.status_code == 200