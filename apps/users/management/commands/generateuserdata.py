#Python modules
from typing import Any
from datetime import datetime
from faker import Faker 
from random import choice, randint
#Django modules
from django.core.management.base import BaseCommand
from django.db.models import QuerySet

#Project modules
from apps.users.models import User

class Command(BaseCommand):
    help = "Generate taks data for testing purposes."
    
    def __generate_users(self,users_count:int=50) -> None:
        fake = Faker("en_US")
        created_users:list[User] = []
        users_before:QuerySet[User] = User.objects.count()
        
        i:int 
        
        for i in range(users_count+1):
            first_name:str = fake.first_name()
            last_name:str = fake.last_name()
            email:str = f"{first_name.lower()[0]}.{last_name.lower()}@example.com"
            phone:str =f"+7{randint(7000000000, 7999999999)}"
            role = User.ROLE_CUSTOMER
            created_users.append(
                User(
                    first_name= first_name,
                    last_name = last_name,
                    email = email,
                    username = email,
                    phone = phone,
                    role = role,
                )
            )
            User.objects.bulk_create(created_users, ignore_conflicts=True)
            users_after = User.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f" Created {users_after - users_before} new users."
            )
        )
        
    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """
        Command Entry point.
        """
        self.__generate_users(users_count=20)
        start_time: datetime = datetime.now()
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                (datetime.now() - start_time.now()).total_seconds()
            )
        )