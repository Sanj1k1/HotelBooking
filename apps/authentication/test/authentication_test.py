import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRegister:
    def test_register_success(self,api_client):
        url = "/api/auth/register/"
        data = {
            "phone":87001110102,
            "email":"Murat@example.com",
            "first_name":"Murat",
            "last_name":"Ramazan",
            "password":"Murat1234",
            "password2":"Murat1234",
            "role":"manager",
        }
        response = api_client.post(url,data)
        
        assert response.status_code == 201
        
    def test_register_duplicate_email(self,api_client,user_customer):
        url = "/api/auth/register/"
        data = {
            "phone":87001110100,
            "email":"Damir@example.com",
            "first_name":"Damir1234",
            "last_name":"Damir",
            "password":"Damir1234",
            "password2":"Damir1234",
            "role":"manager",
        }
        response = api_client.post(url,data)
        
        assert response.status_code == 400
        assert User.objects.filter(email="Damir@example.com").count() == 1
        
    def test_register_invalid_phone(self,api_client):
        url = "/api/auth/register/"
        data = {
            "phone":"hahaha",
            "email":"Damir@example.com",
            "first_name":"Damir1234",
            "last_name":"Damir",
            "password":"Damir1234",
            "password2":"Damir1234",
            "role":"manager",
        }
        response = api_client.post(url,data)
        
        assert response.status_code == 400
        
    def test_register_missing_value(self,api_client):
        url = "/api/auth/register/"
        data = {
            "email":"Damir@example.com",
            "first_name":"Damir1234",
            "last_name":"Damir",
            "password":"Damir1234",
            "password2":"Damir1234",
            "role":"manager",
        }
        response = api_client.post(url,data)
        
        assert response.status_code == 400