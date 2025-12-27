# Python modules
from typing import Any
from datetime import datetime
from faker import Faker
from random import randint

# Django modules
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

# Project modules
from apps.users.models import User


class Command(BaseCommand):
    help = "Generate user data for testing purposes."

    def reset_user_id_sequence(self):
        """Сброс автоинкремента ID (SQLite)."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='users_user';")

    def __generate_users(self, users_count: int = 20) -> None:
        fake = Faker("en_US")

        User.objects.all().delete()
        self.reset_user_id_sequence()

        for i in range(1, users_count + 1):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()[0]}.{last_name.lower()}@gmail.com"
            phone = f"+7{randint(87000000000, 87999999999)}"

            User.objects.create_user(
            phone=phone,
            email=email,
            password="12345678",
            first_name=first_name,
            last_name=last_name,
            role=User.ROLE_CUSTOMER,
            )

        self.stdout.write(self.style.SUCCESS(f"Created {users_count} users with IDs 1–{users_count}"))

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()
        self.__generate_users(users_count=20)
        self.stdout.write(
            self.style.SUCCESS(f"Process finished in {(datetime.now() - start_time).total_seconds()} seconds")
        )
