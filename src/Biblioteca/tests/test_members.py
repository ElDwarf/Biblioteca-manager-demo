import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_unauthorized(client):
   url = reverse('member-list')
   response = client.get(url)
   assert response.status_code == 302