from django.urls import path
from . import views

urlpatterns = [
    # Your other URL patterns
    path('subscribe/', views.subscribe, name='subscribe'),
]