from django.contrib import admin
from django.urls import path

# Временное решение для обхода ошибки
try:
    urlpatterns = [
        path('admin/', admin.site.urls),
    ]
except:
    urlpatterns = []
    print("Admin skipped due to initialization error")