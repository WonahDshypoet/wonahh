from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.homepage, name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('snake_game/', views.snake_game, name='snake_game'),
    path('guess_game/', views.guess_game, name='guess_game'),
]