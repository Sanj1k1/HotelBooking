from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import TemplateView
from apps.core import views  # Импортируем views


def api_home(request):
    """Simple API home endpoint."""
    return JsonResponse({
        'message': 'Hotel Booking API',
        'endpoints': {
            'auth': '/api/auth/',
            'users': '/api/users/',
            'admin': '/admin/',
            'docs': 'Coming soon...',
        }
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include('apps.users.urls')),
    path('', include('apps.core.urls')),
    
    # Frontend pages
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register_page'),
    path('login/', views.login_view, name='login_page'),
    path('profile/', views.profile_view, name='profile_page'),
    
    # API root
    path('api/', api_home, name='api_root'),
]