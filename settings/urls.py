from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

#Swagger
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView


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
            'booking':'/api/booking/',
            'admin': '/admin/',
        }
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.hotels.urls')),
    path('api/',include('apps.booking.urls')),
    # Frontend pages
    path('', include('apps.core.urls')),
    
    # API root
    path('api/', api_home, name='api_root'),
    
    #No-UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    
    #SwaggerUI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]