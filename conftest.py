import pytest 

from rest_framework.test import APIClient

from apps.hotels.models import Hotel

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_customer(db):
    return User.objects.create_user(
            phone=87001110100,
            email="Damir@example.com",
            password="Damir1234",
            first_name="Damir",
            last_name="Temirgali",
            role="customer",
    )

@pytest.fixture
def user_admin(db):
    return User.objects.create_user(
            phone=87001110099,
            email="Daulet@example.com",
            password="Daulet1234",
            first_name="Daulet",
            last_name="Temirgali",
            role="admin",
    )
    
@pytest.fixture
def user_manager(db):
    return User.objects.create_user(
            phone=87001110101,
            email="Sanjar@example.com",
            password="Sanjar1234",
            first_name="Sanjar",
            last_name="Amirgali",
            role="manager",
    )
        
@pytest.fixture
def hotel(db):
    return Hotel.objects.create(
        name="Test Hotel",
        address="Almaty",
        rating=5,
        description="Nice hotel"
    )
    
