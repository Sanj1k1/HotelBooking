# Python modules
from typing import Any
from datetime import datetime
from random import choice, randint
from decimal import Decimal

# Django modules
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.db import connection

# Project modules
from apps.users.models import User
from apps.payment.models import Payment


class Command(BaseCommand):
    help = "Generate payment data for testing purposes."


    def __generate_payment(self) -> None:
        all_users: QuerySet[User] = User.objects.all()

        created_payments: list[Payment] = []
        payment_before = Payment.objects.count()

        for user in all_users:
            amount = Decimal(randint(5000, 50000))  
            method = choice(['credit_card', 'paypal', 'cash'])
            status = choice(['pending', 'completed', 'failed'])

            created_payments.append(
                Payment(
                    user =user,
                    amount=amount,
                    payment_method=method,
                    status=status,
                )
            )

        Payment.objects.bulk_create(created_payments)
        payment_after = Payment.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {payment_after - payment_before} new payments."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()
        self.__generate_payment()
        self.stdout.write(
            f"The whole process took {(datetime.now() - start_time).total_seconds():.2f} seconds."
        )
