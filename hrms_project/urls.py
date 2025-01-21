from django.contrib import admin
from django.urls import path, include
from position_app.views import register_view
urlpatterns = [
    path('admin/', admin.site.urls),
    # Our app URLs
    path('', include('position_app.urls')),

    # Django’s built-in authentication (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_view, name='register'),
]
