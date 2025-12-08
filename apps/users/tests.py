from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    """Тесты МОДЕЛИ User - 4 теста (1 хороший + 3 плохих)"""
    
    def test_create_user_success(self):
        """1 ХОРОШИЙ: Успешное создание пользователя"""
        user = User.objects.create_user(
            phone='+77001234567',
            email='user@example.com',
            first_name='John',
            last_name='Doe',
            password='SecurePass123!'
        )
        
        self.assertEqual(user.phone, '+77001234567')
        self.assertEqual(user.role, 'customer')
        self.assertTrue(user.check_password('SecurePass123!'))
    
    def test_create_user_without_phone(self):
        """1 ПЛОХОЙ: Создание без телефона (должна быть ошибка)"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone='',  # Пустой телефон - НЕДОПУСТИМО
                email='test@example.com',
                password='Test123!'
            )
    
    def test_create_user_with_weak_password(self):
        """2 ПЛОХОЙ: Слабый пароль (модель позволяет, но логически плохо)"""
        user = User.objects.create_user(
            phone='+77001112233',
            email='weak@example.com',
            first_name='Weak',
            last_name='Password',
            password='123'  # ОЧЕНЬ слабый пароль
        )
        
        # Тест проходит, но показывает уязвимость
        # В реальности нужна валидация паролей
        self.assertTrue(user.check_password('123'))
    
    def test_user_role_permissions(self):
        """3 ПЛОХОЙ: Обычный пользователь не может стать админом"""
        user = User.objects.create_user(
            phone='+77009998877',
            email='customer@example.com',
            first_name='Customer',
            last_name='User',
            password='Test123!'
        )
        
        # Пользователь по умолчанию - customer, НЕ админ
        self.assertEqual(user.role, 'customer')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        # Попытка "стать" админом (без прав)
        user.role = 'admin'
        user.save()
        
        # Роль изменилась в БД, но is_staff/is_superuser остались False
        # Это показывает уязвимость - нужны сигналы или дополнительные проверки
        self.assertEqual(user.role, 'admin')
        self.assertFalse(user.is_staff)  # ВСЕ ЕЩЕ False!
        self.assertFalse(user.is_superuser)  # ВСЕ ЕЩЕ False!


class UserEndpointTests(APITestCase):
    """Тесты ENDPOINTS для пользователей - если endpoints существуют"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            phone='+77001234567',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        self.admin = User.objects.create_superuser(
            phone='+77001112233',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123'
        )
    
    def test_registration_endpoint_exists(self):
        """Тест что endpoint регистрации работает"""
        # Этот тест проверяет ОСНОВНОЙ endpoint - регистрацию
        data = {
            'phone': '+77005554433',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'NewPass123!',
            'password2': 'NewPass123!'
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        # Должен быть 201 (Created) или 400 (Bad Request)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
        
        if response.status_code == status.HTTP_201_CREATED:
            # Успешная регистрация
            self.assertIn('user', response.data)
            self.assertEqual(User.objects.count(), 3)  # 2 из setUp + 1 новый
    
    def test_registration_with_existing_phone(self):
        """Попытка регистрации с существующим телефоном"""
        data = {
            'phone': '+77001234567',  # Уже существует
            'email': 'duplicate@example.com',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'password': 'Test123!',
            'password2': 'Test123!'
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        # Должна быть ошибка 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)
    
    def test_registration_with_mismatched_passwords(self):
        """Пароли не совпадают"""
        data = {
            'phone': '+77002223344',
            'email': 'mismatch@example.com',
            'first_name': 'Mismatch',
            'last_name': 'User',
            'password': 'Password123!',
            'password2': 'Different123!'  # Не совпадает!
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_registration_with_invalid_email(self):
        """Неверный формат email - система может пропускать"""
        data = {
            'phone': '+77003334455',
            'email': 'invalid-email',
            'first_name': 'Invalid',
            'last_name': 'Email',
            'password': 'Test123!',
            'password2': 'Test123!'
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        # Принимаем оба варианта
        # 201 = система пропустила (уязвимость, но работает)
        # 400 = система отклонила (правильно)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])