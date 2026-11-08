from django.urls import path

from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.home, name='home'),
    path('science/', views.science, name='science'),
    path('django/', views.django_study, name='django_study'),
    path('science/solar-system/', views.solar_system, name='solar_system'),
]
