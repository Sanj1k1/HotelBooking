import pytest
from rest_framework.test import APIClient
from apps.hotels.models import Hotel, RoomType, Room
from django.contrib.auth import get_user_model
User = get_user_model()

#/api/hotels/ GET request
@pytest.mark.django_db
class TestGetHotels:
    
    #Харош case 1
    def test_get_hotel_success(self,api_client,user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/hotels/"
        response = api_client.get(url)
        
        assert response.status_code == 200

    
    #Не харош case 1 
    def test_get_hotel_unauthored(self,api_client):
        url = "/api/hotels/"
        response = api_client.get(url)
        
        assert response.status_code == 401
    
    #Не харош case 2    
    def test_get_hotels_wrong_url(self,api_client,user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/hotelz/"  
        response = api_client.get(url)
        assert response.status_code == 404
        
    #Не харош case 3 
    def test_get_hotels_method_not_allowed(self, api_client, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/hotels/"
        response = api_client.put(url, data={})
        assert response.status_code == 403


#/api/hotel/{id} GET request
@pytest.mark.django_db
class TestGetHotelbyID:
    
    #Харош case 1
    def test_get_hotel_by_id_success(self, api_client, hotel, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = f"/api/hotels/{hotel.id}/"
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data["id"] == hotel.id
        assert response.data["name"] == hotel.name
        assert response.data["address"] == hotel.address
        assert response.data["rating"] == hotel.rating
        
    #Не харош case 1 
    def test_get_hotel_not_found(self, api_client, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/hotels/10000000000000000000/" 
        response = api_client.get(url)
        
        assert response.status_code == 404

    #Не харош case 2 
    def test_get_hotel_detail_unauthorized(self, api_client, hotel):
        url = f"/api/hotels/{hotel.id}/"
        response = api_client.get(url)
        
        assert response.status_code == 401

    #Не харош case 3
    def test_get_hotel_invalid_id_format(self, api_client, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/hotels/AbylayLoh/"
        response = api_client.get(url)
        
        assert response.status_code == 404
        

#/api/hotel POST request   
@pytest.mark.django_db
class TestCreateHotel:
    
    #Харош case 1
    @pytest.mark.django_db
    def test_create_hotel_success(self, api_client, user_admin):
        api_client.force_authenticate(user=user_admin)
        url = "/api/hotels/"
        hotel = {
            "name": "Abuha hotel",
            "address": "Tole bi street",
            "rating": 1,
            "description": "DO not recommend"
        }   
        response = api_client.post(url, data=hotel)
        
        assert response.status_code in [200, 201]
        assert Hotel.objects.filter(name="Abuha hotel").exists()
        assert response.data["name"] == "Abuha hotel"

    #Не харош case 1 
    def test_create_hotel_forbidden_for_customer(self, api_client, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = "/api/hotels/"
        hotel = {
            "name": "Abuha hotel",
            "address": "Tole bi street",
            "rating": 1,
            "description": "DO not recommend"
        }   
        response = api_client.post(url, data=hotel)
        
        assert response.status_code == 403

    #Не харош case 2 
    def test_create_hotel_unauthorized(self, api_client):
        url = "/api/hotels/"
        hotel = {
            "name": "Abuha hotel",
            "address": "Tole bi street",
            "rating": 1,
            "description": "DO not recommend"
        } 
        response = api_client.post(url, data=hotel)
        
        assert response.status_code == 401

    #Не харош case 3 
    def test_create_hotel_bad_request(self, api_client, user_admin):
        api_client.force_authenticate(user=user_admin)
        url = "/api/hotels/"
        data = {"name": "", "address": "Almaty"}
        response = api_client.post(url, data=data)
        
        assert response.status_code == 400        

#/api/hotel DELETE request
@pytest.mark.django_db
class TestDeleteHotel:
    
    #Харош case 1
    def test_delete_hotel_success(self, api_client, hotel, user_admin):
        api_client.force_authenticate(user=user_admin)
        url = f"/api/hotels/{hotel.id}/"
        response = api_client.delete(url)
        
        assert response.status_code == 204  
        assert not Hotel.objects.filter(id=hotel.id).exists()

    #Не харош case 1
    def test_delete_hotel_not_found(self, api_client, user_admin):
        api_client.force_authenticate(user=user_admin)
        url = "/api/hotels/10000000000000000000/"
        response = api_client.delete(url)
        
        assert response.status_code == 404

    #Не харош case 2
    def test_delete_hotel_unauthorized(self, api_client, hotel):
        url = f"/api/hotels/{hotel.id}/"
        response = api_client.delete(url)
        
        assert response.status_code == 401

    #Не харош case 3
    def test_delete_hotel_forbidden_for_customer(self, api_client, hotel, user_customer):
        api_client.force_authenticate(user=user_customer)
        url = f"/api/hotels/{hotel.id}/"
        response = api_client.delete(url)
        assert response.status_code == 403
        


