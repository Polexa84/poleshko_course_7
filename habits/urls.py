from django.urls import path, include
from rest_framework import routers
from .views import HabitViewSet

router = routers.DefaultRouter()
router.register(r'habits', HabitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]