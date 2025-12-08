from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentSimpleTests(TestCase):
    """Простые тесты модели Payment (4 теста)"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            phone='+77001234567',
            email='test@example.com',
            password='test123'
        )
    
    def test_payment_creation_basic(self):
        """1 ХОРОШИЙ: Базовое создание платежа"""
        # Импортируем здесь чтобы избежать циклических импортов
        from apps.payment.models import Payment
        
        payment = Payment.objects.create(
            user=self.user,
            amount=15000.00,
            payment_method='cash',
            status='pending'
            # Без booking - допустимо при null=True
        )
        
        self.assertEqual(payment.amount, 15000.00)
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.status, 'pending')
    
    def test_payment_string_representation(self):
        """2 ПЛОХОЙ/ХОРОШИЙ: Проверка __str__ метода"""
        from apps.payment.models import Payment
        
        payment = Payment.objects.create(
            user=self.user,
            amount=20000.00,
            payment_method='credit_card',
            status='completed'
        )
        
        str_repr = str(payment)
        self.assertTrue(str_repr)
        self.assertIn(str(payment.amount), str_repr)
    
    def test_payment_status_choices(self):
        """3 ПЛОХОЙ: Проверка валидных статусов"""
        from apps.payment.models import Payment
        
        # Пробуем разные статусы
        test_cases = [
            ('pending', True),
            ('completed', True),
            ('failed', True),
            ('refunded', True),
            ('invalid_status', False),  # Не должно работать
        ]
        
        for status, should_work in test_cases:
            try:
                payment = Payment.objects.create(
                    user=self.user,
                    amount=10000.00,
                    payment_method='paypal',
                    status=status
                )
                if not should_work:
                    self.fail(f"Status '{status}' should not be accepted")
            except Exception:
                if should_work:
                    self.fail(f"Status '{status}' should be accepted")
    
    def test_payment_method_choices(self):
        """4 ПЛОХОЙ: Проверка методов оплаты"""
        from apps.payment.models import Payment
        
        valid_methods = ['credit_card', 'paypal', 'cash', 'bank_transfer']
        
        for method in valid_methods:
            payment = Payment.objects.create(
                user=self.user,
                amount=5000.00,
                payment_method=method,
                status='pending'
            )
            self.assertEqual(payment.payment_method, method)