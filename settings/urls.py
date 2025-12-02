from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_home(request):
    """Simple API home endpoint."""
    return JsonResponse({
        'message': 'Hotel Booking API',
        'endpoints': {
            'auth': '/api/auth/',
            'users': '/api/users/',
            'hotels': '/api/hotels/',
            'rooms': '/api/rooms/',
            'room-types': '/api/room-types/',
            'admin': '/admin/',
        }
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/', include('apps.hotels.urls')),
    
    # Frontend pages
    path('', include('apps.core.urls')),
    
    # API root
    path('api/', api_home, name='api_root'),
]