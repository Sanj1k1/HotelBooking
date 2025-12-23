import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestGetUsers:
    #Хороший case
    def test_get_users_success(self,api_client,user_admin):
        api_client.force_authenticate(user=user_admin)
        url = '/api/users/'
        response = api_client.get(url)
        
        assert response.status_code == 200
        
    #Не Хороший case 1
    def test_get_user_unauthorization(self,api_client):
        url = "/api/users/"
        response = api_client.get(url)
        
        assert response.status_code == 401
    
    #Не Хороший case 2
    def test_get_user_wrong_url(self,api_client,user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/userz/"  
        response = api_client.get(url)
        assert response.status_code == 404      
        
    #Не Хороший case 3    
    def test_get_users_as_customer_shows_only_self(self, api_client, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/users/"
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) == 1 
        assert response.data[0]['id'] == user_customer.id

@pytest.mark.django_db
class TestGetUserbyID:
    #Хороший case
    def test_get_selfuser_success(self, api_client, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = f"/api/users/{user_customer.id}/"
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data['id'] == user_customer.id
    
    #Не Хороший case 1
    def test_get_other_user_forbidden(self, api_client, user_customer, user_admin):
        api_client.force_authenticate(user=user_customer)
        url = f"/api/users/{user_admin.id}/"
        response = api_client.get(url)
        
        assert response.status_code == 403
    
    #Не Хороший case 2    
    def test_get_user_by_id_unauthorized(self, api_client, user_customer):
        url = f"/api/users/{user_customer.id}/"
        response = api_client.get(url)
        
        assert response.status_code == 401
        
    #Не Хороший case 3    
    def test_get_user_not_found(self, api_client, user_admin):
        api_client.force_authenticate(user=user_admin)
        url = "/api/users/99999/"  # Несуществующий ID
        response = api_client.get(url)
        
        assert response.status_code == 404
        
@pytest.mark.django_db   
class TestPutUserbyID:
    #Хороший case
    def test_put_user_success(self,api_client,user_manager):
        api_client.force_authenticate(user=user_manager)
        url = f"/api/users/{user_manager.id}/"
        data = {
            "phone":87001110102,
            "email":"Sanj1k1@example.com",
            "first_name":"Murat",
            "last_name":"Ramazan",
            "role":"manager",
        }
        response = api_client.put(url,data)
        
        assert response.status_code == 200
        assert response.data['phone'] == "87001110102"
        assert response.data["email"] =="Sanj1k1@example.com"
        
    #Не Хороший case 1    
    def test_put_user_unauthorized(self, api_client, user_manager):
        url = f"/api/users/{user_manager.id}/"
        response = api_client.put(url, {"first_name": "Hack"})
        
        assert response.status_code == 401
        
    #Не Хороший case 2    
    def test_put_forbidden_for_other_user(self,api_client,user_customer,user_manager):
        api_client.force_authenticate(user=user_manager)
        url = f"/api/users/{user_customer.id}/"
        data = {
            "phone":87001110201,
            "email":"newemail@sobaka.com"
        }
        response = api_client.put(url,data)
        
        assert response.status_code == 403
    
    #Не Хороший case 3     
    def test_put_user_invalid_data(self,api_client,user_manager):
        api_client.force_authenticate(user=user_manager)
        url = f"/api/users/{user_manager.id}/"
        data = {
            "Abylau":"He's nigga"
        }
        response = api_client.put(url,data)
        
        assert response.status_code == 400
        

@pytest.mark.django_db
class TestPatchUserByID:
    # Хороший case
    def test_patch_user_success(self, api_client, user_manager):
        api_client.force_authenticate(user=user_manager)
        url = f"/api/users/{user_manager.id}/"    
        old_phone = user_manager.phone   
        data = {
            "first_name": "Temirbolat"
        }
        response = api_client.patch(url, data)
        
        assert response.status_code == 200
        assert response.data['first_name'] == "Temirbolat"
        assert str(response.data['phone']) == str(old_phone)

    # Не хороший case 1
    def test_patch_user_unauthorized(self, api_client, user_manager):
        url = f"/api/users/{user_manager.id}/"
        response = api_client.patch(url, {"first_name": "Abuha"})
        
        assert response.status_code == 401

    # Не хороший case 2
    def test_patch_forbidden_for_other_user(self, api_client, user_customer, user_manager):
        api_client.force_authenticate(user=user_manager)
        url = f"/api/users/{user_customer.id}/"
        
        response = api_client.patch(url, {"first_name": "Temirbolat"})
        
        assert response.status_code == 403

    # Не хороший case 3
    def test_patch_user_invalid_data(self, api_client, user_manager):
        api_client.force_authenticate(user=user_manager)
        url = f"/api/users/{user_manager.id}/"
        
        data = {
            "email": "hahaha"
        }
        response = api_client.patch(url, data)
        
        assert response.status_code == 400
        assert "email" in response.data        
        
        
        
@pytest.mark.django_db         
class TestDeleteUserByID:
    def test_delete_user_success(self,api_client,user_customer):
        api_client.force_authenticate(user=user_customer)
        url = f"/api/users/{user_customer.id}/"
        response = api_client.delete(url)
        
        assert response.status_code == 204
        assert not User.objects.filter(id=user_customer.id).exists()
        
    #Не Хороший case 1    
    def test_delete_user_unauthorized(self, api_client, user_customer):
        url = f"/api/users/{user_customer.id}/"
        response = api_client.delete(url)
        
        assert response.status_code == 401
        
    #Не Хороший case 2    
    def test_delete_forbidden_for_other_user(self,api_client,user_customer,user_manager):
        api_client.force_authenticate(user=user_manager)
        url = f"/api/users/{user_customer.id}/"
        response = api_client.delete(url)
        
        assert response.status_code == 403
    
    #Не Хороший case 3     
    def test_delete_user_not_found(self, api_client, user_admin):
        api_client.force_authenticate(user=user_admin)
        url = "/api/users/10000000000000000000/"
        response = api_client.delete(url)
        
        assert response.status_code == 404
        
        
        