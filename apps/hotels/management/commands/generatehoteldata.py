#Python modules
from datetime import datetime
from typing import Any
from random import uniform,choice
#Django moduesl
from django.core.management.base import BaseCommand
from django.db.models import QuerySet

#Project modules
from apps.hotels.models import Hotel,Room,RoomType

class Command(BaseCommand):
    help = "Generate taks data for testing purposes."
    
    HOTELS = [
        {"name": "Grand Horizon Hotel", "address": "123 Ocean Drive, Miami, USA"},
        {"name": "Emerald Palace", "address": "45 Green Street, London, UK"},
        {"name": "Blue Lagoon Resort", "address": "78 Beach Avenue, Honolulu, USA"},
        {"name": "Royal Orchid Inn", "address": "22 Rajpath Road, New Delhi, India"},
        {"name": "Mountain View Lodge", "address": "9 Alpine Way, Zurich, Switzerland"},
        {"name": "The Velvet Sky", "address": "12 Sunset Blvd, Los Angeles, USA"},
        {"name": "Ocean Breeze Hotel", "address": "34 Marine Drive, Cape Town, South Africa"},
        {"name": "Silver Leaf Boutique", "address": "89 Queen Street, Toronto, Canada"},
        {"name": "Golden Sands Resort", "address": "76 Palm Road, Dubai, UAE"},
        {"name": "Crystal Bay Hotel", "address": "105 Seaside Blvd, Sydney, Australia"},
        {"name": "UrbanStay Hotel", "address": "23 Downtown Street, New York, USA"},
        {"name": "MetroLux Suites", "address": "14 Business Ave, Singapore"},
        {"name": "Skyline Residence", "address": "88 Tower Lane, Hong Kong"},
        {"name": "Nova Business Inn", "address": "56 Innovation Park, Berlin, Germany"},
        {"name": "Platinum Tower Hotel", "address": "7 Main Square, Warsaw, Poland"},
        {"name": "Executive Plaza", "address": "31 Corporate Blvd, Chicago, USA"},
        {"name": "Zenith Grand Hotel", "address": "17 Central Avenue, Paris, France"},
        {"name": "Capital Crown Hotel", "address": "50 City Center, Astana, Kazakhstan"},
        {"name": "Velocity Inn", "address": "14 Express Road, Tokyo, Japan"},
        {"name": "Axis Central Suites", "address": "66 Downtown Plaza, Seoul, South Korea"},
        {"name": "Aurora Peak Lodge", "address": "27 Glacier Way, Reykjavik, Iceland"},
        {"name": "Desert Mirage Resort", "address": "91 Sand Dune Rd, Doha, Qatar"},
        {"name": "Whispering Pines Retreat", "address": "33 Forest Trail, Vancouver, Canada"},
        {"name": "Sunset Boulevard Inn", "address": "15 Sunset Street, Los Angeles, USA"},
        {"name": "Arctic Breeze Hotel", "address": "72 Polar Avenue, Oslo, Norway"},
        {"name": "Moonlight Haven", "address": "39 Dream Lane, Kyoto, Japan"},
        {"name": "Serenity Springs", "address": "25 Waterfall Road, Auckland, New Zealand"},
        {"name": "Coral Reef Resort", "address": "60 Island Blvd, Maldives"},
        {"name": "Majestic Valley Hotel", "address": "8 Riverbank Way, Almaty, Kazakhstan"},
        {"name": "Sapphire Coast Retreat", "address": "101 Ocean View, Lisbon, Portugal"},
    ]

    DEFAULT_ROOM_TYPES = [
        {"name": "Single", "capacity": 1},
        {"name": "Double", "capacity": 2},
        {"name": "Deluxe", "capacity": 2},
        {"name": "Suite", "capacity": 3},
    ]
    
    def __generate_hotels(self) -> None:
        """
        Generate hotels for testing data.
        """
        created_hotels: list[Hotel] = []
        hotels_before : QuerySet[Hotel] = Hotel.objects.count()
        
        i:int
        
        for i in self.HOTELS:
            name:str = f'{i['name']}'
            address: str = f"{i["address"]}"
            rating: int = round(uniform(3.0,5.0),1)
            created_hotels.append(
                Hotel(
                    name = name,
                    address = address,
                    rating = rating,
                )
            )
        Hotel.objects.bulk_create(created_hotels,ignore_conflicts=True)
        hotels_after:int = Hotel.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {hotels_after - hotels_before} hotels."
            )
        )
        
    def __generate_roomtype(self) -> None:
        """
        Generate roomtype testing data for hotels.
        """
        existing_count = Room.objects.count()
        if existing_count == 0:
            RoomType.objects.bulk_create(
                [RoomType(**roomtype) for roomtype in self.DEFAULT_ROOM_TYPES],
                ignore_conflicts=True
            )
        else:
            self.stdout.write(self.style.WARNING(f" Room types already exist ({existing_count} found)."))
            
    
    def __generate_rooms(self,rooms_per_hotel:int= 100) -> None:
        """
        Generate rooms testing data for hotels.
        """
        hotels:Hotel = Hotel.objects.all()
        room_types:Room = list(RoomType.objects.all())
        i:int 
        total_rooms:int = 0
        for hotel in hotels:
            rooms_created:list[Room] = []
            for i in range(1,rooms_per_hotel+1):
                rooms_created.append(
                    Room(
                        number = str(i),
                        price_per_night = round(uniform(60,350),2),
                        is_available = True,
                        hotel = hotel,
                        RoomType=choice(room_types),
                    )
                )
            Room.objects.bulk_create(rooms_created,ignore_conflicts=True)
            total_rooms +=len(rooms_created)
            
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {total_rooms} rooms in hotels."
            )
        )    
                
        
        
    
    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """
        Command Entry point.
        """
        
        start_time: datetime = datetime.now()
        self.__generate_roomtype()
        self.__generate_hotels()
        self.__generate_rooms(rooms_per_hotel=20)
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                (datetime.now() - start_time.now()).total_seconds()
            )
        )