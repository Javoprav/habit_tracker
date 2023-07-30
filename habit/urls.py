from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()
router.register(r'habits', HabitsViewSet, basename='habits')


urlpatterns = [

              ] + router.urls
