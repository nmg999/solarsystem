from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='learning/login.html',
        next_page='learning:home',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='learning:home'), name='logout'),
    path('science/', views.science, name='science'),
    path('django/', views.django_study, name='django_study'),
    path('science/solar-system/', views.solar_system, name='solar_system'),
]
