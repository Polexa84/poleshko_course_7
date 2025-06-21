from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('habits.urls')),  # Добавляем URL-адреса приложения habits
    path('api/users/', include('users.urls')),  # Добавляем URL-адреса приложения users
]