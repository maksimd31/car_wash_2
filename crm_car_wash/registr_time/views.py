from django.shortcuts import render
from django.contrib.sites import requests
from django.views.decorators.http import require_http_methods
# from .models import Client
# from .forms import SignUpForm, AddRecordClientForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core import management
import requests

# from crm_car_wash.registr_time.forms import SignUpForm
from .forms import SignUpForm


# from crm_car_wash.registr_time.forms import SignUpForm


# Create your views here.

def authenticated_user_required(view_func):
    """
        Декоратор, требующий аутентификацию пользователя.

        Этот декоратор проверяет, является ли пользователь аутентифицированным.
        Если пользователь аутентифицирован, он вызывает исходную функцию представления.
        В противном случае он перенаправляет пользователя на домашнюю страницу с сообщением, что необходимо войти
         в систему.

        Args:
            view_func (function): Функция представления, которую требуется защитить.

        Returns:
            function: Обертка для функции представления.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.success(request, "Необходимо войти в систему...")
            return redirect('home_registr')

    return wrapper

def home_registr(request):
    """
        Обрабатывает запрос на главную страницу.

        Если метод запроса - POST, пытается аутентифицировать пользователя.
        Если аутентификация прошла успешно, производит вход пользователя и перенаправляет на главную страницу.
        В противном случае отправляет сообщение об ошибке и также перенаправляет на главную страницу.

        Если метод запроса не POST, просто рендерит главную страницу.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли!")
            return redirect('home_registr')
        else:
            messages.success(request, "ERROR ОШИБКА Please Try Again...")
            return redirect('home_registr')
    else:
        return render(request, 'home_registr.html')


def register_user(request):
    """
        Регистрирует нового пользователя.

        Если метод запроса POST, форма SignUpForm заполняется данными из запроса.
        Если форма валидна, сохраняет форму, аутентифицирует пользователя и осуществляет вход.
        Затем отправляет сообщение об успехе и перенаправляет на домашнюю страницу.
        Если форма не валидна, возвращает страницу регистрации с этой формой.

        Если метод запроса не POST, возвращает страницу регистрации с новой формой SignUpForm.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Вы Успешно Зарегистрировались! Добро пожаловать!")
            return redirect('home_registr')
    else:
        form = SignUpForm()
        return render(request, 'register_reg.html', {'form': form})

    return render(request, 'register_reg.html', {'form': form})


def logout_user(request):
    """
       Выход пользователя из системы.

       Эта функция выполняет выход пользователя из системы.
       После выхода, пользователю показывается сообщение об успешном выходе, и
       происходит перенаправление на домашнюю страницу.

       Параметры:
       request (HttpRequest): HTTP запрос от клиента.

       Возвращает:
       HttpResponseRedirect: перенаправление на домашнюю страницу.
    """
    logout(request)
    messages.success(request, "Вы вышли из системы")
    return redirect('home_registr')


#Регистрация времени
def register_start(request):
    pass

def register_stop(request):
    pass

def register_total(request):
    pass


# def home_reg():
#     return None
#
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Timer
# import time
#
# @authenticated_user_required
# def timer_view(request):
#     timer, created = Timer.objects.get_or_create(user=request.user)
#
#     if request.method == "POST":
#         if 'start' in request.POST:
#             timer.start_time = time.time()
#             timer.intervals = []
#             timer.save()
#         elif 'stop' in request.POST:
#             if timer.start_time:
#                 interval = time.time() - timer.start_time
#                 timer.elapsed_time += interval
#                 timer.intervals.append(interval)
#                 timer.start_time = None
#                 timer.save()
#
#     total_time = timer.elapsed_time + sum(timer.intervals)
#     return render(request, 'timer.html', {
#         'total_time': total_time,
#         'intervals': timer.intervals,
#     })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Timer
import time

@login_required
def timer_view(request):
    timer, created = Timer.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if 'start' in request.POST:
            timer.start_time = time.time()
            timer.intervals = []
            timer.save()
        elif 'stop' in request.POST:
            if timer.start_time is not None:  # Проверка на наличие start_time
                interval = time.time() - timer.start_time
                timer.elapsed_time += interval
                timer.intervals.append(interval)
                timer.start_time = None
                timer.save()

    total_time = timer.elapsed_time + sum(timer.intervals)
    return render(request, 'timer.html', {
        'total_time': total_time,
        'intervals': timer.intervals,
    })