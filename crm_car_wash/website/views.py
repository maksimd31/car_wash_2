from django.shortcuts import render
# Импортируем аутентификацию
from django.contrib.auth import authenticate, login, logout
# импортируем со0бщения
from django.contrib import messages


# Create your views here.

def home(request):
    """Отрисуем главную страницу"""
    return render(request, 'home.html', {})


def login_user(request):
    """фукция входа"""
    pass


def logout_user(request):
    """Функция выхода"""
    pass
