from django.conf import settings
from django.http import FileResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


def home(request):
    return render(request, 'learning/home.html')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('learning:home')
    form = UserCreationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('learning:home')
    return render(request, 'learning/signup.html', {'form': form})


def science(request):
    return render(request, 'learning/science.html')


def django_study(request):
    return render(request, 'learning/django.html')


def solar_system(request):
    return FileResponse(
        (settings.BASE_DIR / 'solar_system.html').open('rb'),
        content_type='text/html; charset=utf-8',
    )

# Create your views here.
