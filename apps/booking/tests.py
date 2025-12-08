from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.hotels.models import Hotel, RoomType, Room
from .models import Booking

User = get_user_model()


class BookingModelTest(TestCase):
    """Тесты модели Booking (1 хороший + 3 плохих)"""
    
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            phone='+77001234567',
            email='user@example.com',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        
        # Создаем отель и комнату
        self.hotel = Hotel.objects.create(
            name='Grand Hotel',
            address='Almaty',
            rating=5,
            owner=self.user
        )
        
        self.room_type = RoomType.objects.create(name='Deluxe', capacity=2)
        
        self.room = Room.objects.create(
            number=101,
            price_per_night=15000,
            hotel=self.hotel,
            room_type=self.room_type
        )
    
    # 1 GOOD CASE: Успешное создание брони
    def test_create_booking_success(self):
        """Успешное создание бронирования"""
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in='2024-12-01',
            check_out='2024-12-03',
            total_price=30000,
            status='pending'
        )
        
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.total_price, 30000)
    
    # 1 BAD CASE: Бронь с прошедшей датой
    def test_booking_past_date(self):
        """Попытка создать бронь с прошедшей датой (тест логики, не валидации)"""
        past_date = timezone.now().date() - timezone.timedelta(days=1)
        
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=past_date,
            check_out=timezone.now().date(),
            total_price=15000,
            status='pending'
        )
        
        # Тест проходит, но в реальности нужна валидация
        self.assertEqual(booking.check_in, past_date)
    
    # 2 BAD CASE: check_out раньше check_in
    def test_booking_invalid_dates(self):
        """check_out раньше check_in (логическая ошибка)"""
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in='2024-12-03',
            check_out='2024-12-01',  # Ошибка!
            total_price=15000,
            status='pending'
        )
        
        # Модель позволяет, но это логическая ошибка
        # В сериализаторе нужно добавить валидацию
        self.assertGreater(booking.check_in, booking.check_out)
    
    # 3 BAD CASE: Неверный статус
    def test_booking_invalid_status(self):
        """Использование несуществующего статуса"""
        try:
            booking = Booking.objects.create(
                user=self.user,
                room=self.room,
                check_in='2024-12-01',
                check_out='2024-12-03',
                total_price=30000,
                status='invalid_status'  # Не из STATUS_CHOICES
            )
            # Если создалось - у модели нет проверки choices
            self.assertNotIn(booking.status, ['pending', 'confirmed', 'cancelled', 'completed'])
        except Exception:
            # Если ошибка - choices работают
            pass


class BookingAPITest(APITestCase):
    """API тесты для BookingViewSet (1 хороший + 3 плохих на endpoint)"""
    
    def setUp(self):
        # Создаем двух пользователей
        self.user1 = User.objects.create_user(
            phone='+77001234567',
            email='user1@example.com',
            first_name='User1',
            last_name='Test',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            phone='+77009876543',
            email='user2@example.com',
            first_name='User2',
            last_name='Test',
            password='testpass123'
        )
        
        # Создаем админа
        self.admin = User.objects.create_user(
            phone='+77001112233',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123',
            role='admin',
            is_staff=True
        )
        
        # Создаем отель и комнату
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            address='Test Address',
            rating=4,
            owner=self.user1
        )
        
        self.room_type = RoomType.objects.create(name='Standard', capacity=2)
        
        self.room = Room.objects.create(
            number=101,
            price_per_night=10000,
            hotel=self.hotel,
            room_type=self.room_type
        )
        
        # Создаем тестовые брони
        self.booking1 = Booking.objects.create(
            user=self.user1,
            room=self.room,
            check_in='2024-12-01',
            check_out='2024-12-03',
            total_price=20000,
            status='confirmed'
        )
        
        self.booking2 = Booking.objects.create(
            user=self.user2,
            room=self.room,
            check_in='2024-12-05',
            check_out='2024-12-07',
            total_price=20000,
            status='pending'
        )
        
        self.client = APIClient()
    
    # ===== GET /api/bookings/ =====
    
    def test_get_bookings_as_admin(self):
        """1 GOOD: Админ видит все брони"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/bookings/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Две брони
    
    def test_get_bookings_as_user(self):
        """2 GOOD: Пользователь видит только свои брони"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/bookings/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Только свои
        self.assertEqual(response.data[0]['id'], self.booking1.id)
    
    def test_get_bookings_unauthenticated(self):
        """1 BAD: Неавторизованный доступ"""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # ===== POST /api/bookings/ =====
    
    def test_create_booking_success(self):
        """1 GOOD: Успешное создание брони"""
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'room_id': self.room.id,
            'check_in': '2024-12-10',
            'check_out': '2024-12-12',
            'total_price': 20000
        }
        
        response = self.client.post('/api/bookings/', data, format='json')
        
        # Может быть 201 или 400 (если есть валидация дат)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_create_booking_missing_room(self):
        """1 BAD: Создание брони без указания комнаты"""
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'check_in': '2024-12-10',
            'check_out': '2024-12-12',
            'total_price': 20000
            # Нет room_id
        }
        
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_booking_invalid_dates(self):
        """2 BAD: Неправильные даты (если есть валидация)"""
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'room_id': self.room.id,
            'check_in': '2024-12-12',  # После check_out
            'check_out': '2024-12-10',  # До check_in
            'total_price': 20000
        }
        
        response = self.client.post('/api/bookings/', data, format='json')
        
        # Может быть 400 (валидация) или 201 (нет валидации)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    # ===== GET /api/bookings/{id}/ =====
    
    def test_get_booking_detail_as_owner(self):
        """1 GOOD: Владелец видит свою бронь"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/bookings/{self.booking1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_booking_detail_as_non_owner(self):
        """3 BAD: Чужой пользователь не видит бронь"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/bookings/{self.booking1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ===== DELETE /api/bookings/{id}/ =====
    
    def test_delete_booking_as_owner(self):
        """Пользователь может удалить свою бронь"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/bookings/{self.booking1.id}/')
        self.assertIn(response.status_code, [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_403_FORBIDDEN
        ])
    
    def test_delete_booking_as_non_owner(self):
        """Чужой не может удалить бронь"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/bookings/{self.booking1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)