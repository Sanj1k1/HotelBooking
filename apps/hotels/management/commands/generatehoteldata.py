#Python modules
from datetime import datetime
from typing import Any
from random import uniform,choice

#Django moduesl
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.db import connection

#Project modules
from apps.hotels.models import Hotel,Room,RoomType
from apps.users.models import User


class Command(BaseCommand):
    help = "Generate taks data for testing purposes."
    
    HOTELS = [
    {
        "name": "Grand Horizon Hotel",
        "address": "123 Ocean Drive, Miami, USA",
        "owner": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+77000000001",
            "email": "john.doe@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Emerald Palace",
        "address": "45 Green Street, London, UK",
        "owner": {
            "first_name": "Alice",
            "last_name": "Smith",
            "phone": "+77000000002",
            "email": "alice.smith@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Blue Lagoon Resort",
        "address": "78 Beach Avenue, Honolulu, USA",
        "owner": {
            "first_name": "Michael",
            "last_name": "Brown",
            "phone": "+77000000003",
            "email": "michael.brown@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Royal Orchid Inn",
        "address": "22 Rajpath Road, New Delhi, India",
        "owner": {
            "first_name": "Emma",
            "last_name": "Johnson",
            "phone": "+77000000004",
            "email": "emma.johnson@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Mountain View Lodge",
        "address": "9 Alpine Way, Zurich, Switzerland",
        "owner": {
            "first_name": "William",
            "last_name": "Lee",
            "phone": "+77000000005",
            "email": "william.lee@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "The Velvet Sky",
        "address": "12 Sunset Blvd, Los Angeles, USA",
        "owner": {
            "first_name": "Olivia",
            "last_name": "Davis",
            "phone": "+77000000006",
            "email": "olivia.davis@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Ocean Breeze Hotel",
        "address": "34 Marine Drive, Cape Town, South Africa",
        "owner": {
            "first_name": "James",
            "last_name": "Wilson",
            "phone": "+77000000007",
            "email": "james.wilson@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Silver Leaf Boutique",
        "address": "89 Queen Street, Toronto, Canada",
        "owner": {
            "first_name": "Sophia",
            "last_name": "Taylor",
            "phone": "+77000000008",
            "email": "sophia.taylor@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Golden Sands Resort",
        "address": "76 Palm Road, Dubai, UAE",
        "owner": {
            "first_name": "Benjamin",
            "last_name": "Anderson",
            "phone": "+77000000009",
            "email": "benjamin.anderson@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Crystal Bay Hotel",
        "address": "105 Seaside Blvd, Sydney, Australia",
        "owner": {
            "first_name": "Isabella",
            "last_name": "Thomas",
            "phone": "+77000000010",
            "email": "isabella.thomas@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "UrbanStay Hotel",
        "address": "23 Downtown Street, New York, USA",
        "owner": {
            "first_name": "Liam",
            "last_name": "Martinez",
            "phone": "+77000000011",
            "email": "liam.martinez@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "MetroLux Suites",
        "address": "14 Business Ave, Singapore",
        "owner": {
            "first_name": "Mia",
            "last_name": "Garcia",
            "phone": "+77000000012",
            "email": "mia.garcia@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Skyline Residence",
        "address": "88 Tower Lane, Hong Kong",
        "owner": {
            "first_name": "Ethan",
            "last_name": "Rodriguez",
            "phone": "+77000000013",
            "email": "ethan.rodriguez@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Nova Business Inn",
        "address": "56 Innovation Park, Berlin, Germany",
        "owner": {
            "first_name": "Charlotte",
            "last_name": "Lopez",
            "phone": "+77000000014",
            "email": "charlotte.lopez@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Platinum Tower Hotel",
        "address": "7 Main Square, Warsaw, Poland",
        "owner": {
            "first_name": "Henry",
            "last_name": "Gonzalez",
            "phone": "+77000000015",
            "email": "henry.gonzalez@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Executive Plaza",
        "address": "31 Corporate Blvd, Chicago, USA",
        "owner": {
            "first_name": "Amelia",
            "last_name": "Hernandez",
            "phone": "+77000000016",
            "email": "amelia.hernandez@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Zenith Grand Hotel",
        "address": "17 Central Avenue, Paris, France",
        "owner": {
            "first_name": "Alexander",
            "last_name": "King",
            "phone": "+77000000017",
            "email": "alexander.king@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Capital Crown Hotel",
        "address": "50 City Center, Astana, Kazakhstan",
        "owner": {
            "first_name": "Harper",
            "last_name": "Wright",
            "phone": "+77000000018",
            "email": "harper.wright@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Velocity Inn",
        "address": "14 Express Road, Tokyo, Japan",
        "owner": {
            "first_name": "Daniel",
            "last_name": "Lopez",
            "phone": "+77000000019",
            "email": "daniel.lopez@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Axis Central Suites",
        "address": "66 Downtown Plaza, Seoul, South Korea",
        "owner": {
            "first_name": "Ella",
            "last_name": "Hill",
            "phone": "+77000000020",
            "email": "ella.hill@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Aurora Peak Lodge",
        "address": "27 Glacier Way, Reykjavik, Iceland",
        "owner": {
            "first_name": "Lucas",
            "last_name": "Scott",
            "phone": "+77000000021",
            "email": "lucas.scott@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Desert Mirage Resort",
        "address": "91 Sand Dune Rd, Doha, Qatar",
        "owner": {
            "first_name": "Lily",
            "last_name": "Adams",
            "phone": "+77000000022",
            "email": "lily.adams@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Whispering Pines Retreat",
        "address": "33 Forest Trail, Vancouver, Canada",
        "owner": {
            "first_name": "Owen",
            "last_name": "Baker",
            "phone": "+77000000023",
            "email": "owen.baker@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Sunset Boulevard Inn",
        "address": "15 Sunset Street, Los Angeles, USA",
        "owner": {
            "first_name": "Chloe",
            "last_name": "Carter",
            "phone": "+77000000024",
            "email": "chloe.carter@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Arctic Breeze Hotel",
        "address": "72 Polar Avenue, Oslo, Norway",
        "owner": {
            "first_name": "Nathan",
            "last_name": "Evans",
            "phone": "+77000000025",
            "email": "nathan.evans@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Moonlight Haven",
        "address": "39 Dream Lane, Kyoto, Japan",
        "owner": {
            "first_name": "Ava",
            "last_name": "Green",
            "phone": "+77000000026",
            "email": "ava.green@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Serenity Springs",
        "address": "25 Waterfall Road, Auckland, New Zealand",
        "owner": {
            "first_name": "Jack",
            "last_name": "Hall",
            "phone": "+77000000027",
            "email": "jack.hall@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Coral Reef Resort",
        "address": "60 Island Blvd, Maldives",
        "owner": {
            "first_name": "Grace",
            "last_name": "Young",
            "phone": "+77000000028",
            "email": "grace.young@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Majestic Valley Hotel",
        "address": "8 Riverbank Way, Almaty, Kazakhstan",
        "owner": {
            "first_name": "Henry",
            "last_name": "Kingston",
            "phone": "+77000000029",
            "email": "henry.kingston@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    {
        "name": "Sapphire Coast Retreat",
        "address": "101 Ocean View, Lisbon, Portugal",
        "owner": {
            "first_name": "Ella",
            "last_name": "Foster",
            "phone": "+77000000030",
            "email": "ella.foster@example.com",
            "role": "manager",
            "password": "12345678"
        }
    },
    ]

    DEFAULT_ROOM_TYPES = [
        {"name": "Single", "capacity": 1},
        {"name": "Double", "capacity": 2},
        {"name": "Deluxe", "capacity": 2},
        {"name": "Suite", "capacity": 3},
    ]
    
    def __reset_sequence(self, table_name: str):
        """Сброс автоинкремента ID для SQLite."""
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
        self.stdout.write(self.style.WARNING(f"ID sequence for {table_name} reset."))
    
    def __clear_data(self) -> None:
        """Clear all existing data and reset sequences."""
        Room.objects.all().delete()
        Hotel.objects.all().delete()
        RoomType.objects.all().delete()

        self.__reset_sequence("hotels_hotel")
        self.__reset_sequence("hotels_room")
        self.__reset_sequence("hotels_roomtype")

        self.stdout.write(self.style.WARNING("Cleared all data and reset ID sequences."))
        
    def __generate_hotels(self,rooms_per_hotel=20) -> None:
        """
        Generate hotels for testing data.
        """
        created_hotels: list[Hotel] = []
        hotels_before : QuerySet[Hotel] = Hotel.objects.count()
        
        hotel_data:int
        
        for hotel_data in self.HOTELS:
            owner_data = hotel_data.get("owner")
            if owner_data:
                user, created = User.objects.get_or_create(
                    phone = owner_data["phone"],
                    defaults={
                    "first_name": owner_data["first_name"],
                    "last_name": owner_data["last_name"],
                    "email": owner_data["email"],
                    "role": owner_data.get("role", User.ROLE_MANAGER),
                    }
                )
                if created:
                    user.set_password(owner_data["password"])
                    user.save()
            else:
                user = None 
            
            hotel = Hotel.objects.create(
                name=hotel_data["name"],
                address=hotel_data["address"],
                rating=round(uniform(3.0, 5.0), 1),
                owner=user,
            )

            hotels_after:int = Hotel.objects.count()
            
            room_types = list(RoomType.objects.all())
            rooms_created = []
            for i in range(1,rooms_per_hotel+1):
                rooms_created.append(
                    Room(
                        number=i,
                        price_per_night=round(uniform(60, 350), 2),
                        is_available=choice([True, False]),
                        hotel=hotel,
                        room_type=choice(room_types),
                    )
                )
            Room.objects.bulk_create(rooms_created)
            created_hotels.append(hotel)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(created_hotels)} hotels with 20 rooms each."
                )
            )
        
    def __generate_roomtype(self) -> None:
        """
        Generate roomtype testing data for hotels.
        """
        existing_count = RoomType.objects.count()
        if existing_count == 0:
            RoomType.objects.bulk_create(
                [RoomType(**roomtype) for roomtype in self.DEFAULT_ROOM_TYPES],
                ignore_conflicts=True
            )
        else:
            self.stdout.write(self.style.WARNING(f" Room types already exist ({existing_count} found)."))
            
    
    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """
        Command Entry point.
        """
        
        start_time: datetime = datetime.now()
        
        self.__clear_data()
        
        self.__generate_roomtype()
        self.__generate_hotels(rooms_per_hotel=20)
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                (datetime.now() - start_time.now()).total_seconds()
            )
        )