import pytest 

from rest_framework.test import APIClient

from apps.hotels.models import Hotel,RoomType,Room

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
            phone=87001110099,
            email="Dauka@example.com",
            password="Dauka1234",
            first_name="Dauka",
            last_name="Daukovich",
            role="customer",
    )
    
@pytest.fixture
def hotel(db):
    return Hotel.objects.create(
        name="Test Hotel",
        address="Almaty",
        rating=5,
        description="Nice hotel"
    )
    
