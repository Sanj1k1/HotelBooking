from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AuthenticationTest(APITestCase):
    """Тесты для аутентификации - РАБОЧИЕ И ПРОСТЫЕ"""
    
    def setUp(self):
        # URL endpoints
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/token/'
        self.refresh_url = '/api/auth/token/refresh/'
        
        # Данные для регистрации
        self.valid_user_data = {
            'phone': '+77001234567',
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        
        # Создаем пользователя для тестов логина
        self.existing_user = User.objects.create_user(
            phone='+77009876543',
            email='existing@example.com',
            first_name='Existing',
            last_name='User',
            password='ExistingPass123!'
        )
    
    # ===== РЕГИСТРАЦИЯ =====
    
    def test_register_success(self):
        """Тест 1: Успешная регистрация (GOOD)"""
        response = self.client.post(
            self.register_url,
            self.valid_user_data,
            format='json'
        )
        
        # Проверяем что пользователь создан
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(User.objects.count(), 2)  # 1 existing + 1 new
    
    def test_register_missing_phone(self):
        """Тест 2: Регистрация без телефона (BAD)"""
        data = self.valid_user_data.copy()
        data.pop('phone')  # Убираем телефон
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)
    
    def test_register_passwords_not_match(self):
        """Тест 3: Пароли не совпадают (BAD)"""
        data = self.valid_user_data.copy()
        data['password2'] = 'DifferentPass123!'  # Не совпадает
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_duplicate_phone(self):
        """Тест 4: Дубликат телефона (BAD)"""
        # Сначала успешная регистрация
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Пытаемся зарегистрироваться с тем же телефоном
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        
        response = self.client.post(self.register_url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ===== ЛОГИН =====
    
    def test_login_success(self):
        """Тест 5: Успешный логин (GOOD)"""
        login_data = {
            'phone': '+77009876543',  # Существующий пользователь
            'password': 'ExistingPass123!'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_wrong_password(self):
        """Тест 6: Неверный пароль (BAD)"""
        login_data = {
            'phone': '+77009876543',
            'password': 'WrongPassword123!'  # Неверный пароль
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Тест 7: Несуществующий пользователь (BAD)"""
        login_data = {
            'phone': '+77000000000',  # Не существует
            'password': 'SomePass123!'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_empty_data(self):
        """Тест 8: Пустые данные (BAD)"""
        response = self.client.post(self.login_url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)
        self.assertIn('password', response.data)
    
    # ===== REFRESH TOKEN =====
    
    def test_refresh_token(self):
        """Тест 9: Обновление токена"""
        # Сначала логинимся чтобы получить refresh токен
        login_data = {
            'phone': '+77009876543',
            'password': 'ExistingPass123!'
        }
        
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Обновляем токен
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(self.refresh_url, refresh_data, format='json')
        
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)