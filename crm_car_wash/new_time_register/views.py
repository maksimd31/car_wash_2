from datetime import time, timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.datetime_safe import datetime

from .forms import SignUpForm


# from django.shortcuts import render, redirect

# from .models import Timer, TimeSegment


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


from django.shortcuts import render, redirect
from .models import TimeInterval, DailySummary
from django.utils import timezone

import pytz

#
# @authenticated_user_required
# def time_interval_view(request):
#     if request.method == 'POST':
#         moscow_tz = pytz.timezone('Europe/Moscow')
#
#         if 'start' in request.POST:
#             # Записываем текущее московское время в start_time
#             # moscow_tz = pytz.timezone('Europe/Moscow')
#             interval = TimeInterval(user=request.user, start_time=timezone.now().astimezone(moscow_tz).time())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.filter(user=request.user).last()
#             if interval:
#                 interval.end_time = timezone.now().astimezone(moscow_tz).time()
#                 interval.save()
#
#                 # Обновляем DailySummary
#                 date_key = timezone.now().astimezone(moscow_tz).date()
#                 daily_summary, created = DailySummary.objects.get_or_create(date=date_key)
#                 daily_summary.interval_count += 1
#                 daily_summary.total_duration += interval.duration
#                 daily_summary.save()
#
#             return redirect('time_interval_view')
#
#         elif 'reset' in request.POST:
#             # Удаляем все записи из модели TimeInterval
#             TimeInterval.objects.all().delete()
#             return redirect('time_interval_view')
#
#     intervals = TimeInterval.objects.all()
#     formatted_intervals = []
#
#     for interval in intervals:
#         if interval.start_time and interval.end_time:
#             duration = interval.duration
#             minutes, seconds = divmod(duration.total_seconds(), 60)
#             formatted_intervals.append({
#                 'start_time': interval.start_time.strftime("%H:%M:%S"),
#                 'end_time': interval.end_time.strftime("%H:%M:%S"),
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"})
#
#             # Получаем сводные данные по дням
#     daily_summary = DailySummary.objects.all()
#     formatted_summary = []
#
#     for summary in daily_summary:
#         if summary.total_duration:
#             total_seconds = int(summary.total_duration.total_seconds())
#             hours, remainder = divmod(total_seconds, 3600)
#             minutes, seconds = divmod(remainder, 60)
#             formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
#         else:
#             formatted_duration = "00:00:00"
#
#         formatted_summary.append({
#             'date': summary.date,
#             'interval_count': summary.interval_count,
#             'total_duration': formatted_duration,
#         })
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summary': formatted_summary
#     })

# import pytz
# from django.utils import timezone
# # from django.contrib.auth.decorators import login_required
#
# @authenticated_user_required
# def time_interval_view(request):
#     moscow_tz = pytz.timezone('Europe/Moscow')
#
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее московское время в start_time
#             interval = TimeInterval(user=request.user, start_time=timezone.now().astimezone(moscow_tz).time())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.filter(user=request.user).last()
#             if interval:
#                 interval.end_time = timezone.now().astimezone(moscow_tz).time()
#                 interval.save()
#
#                 # Обновляем DailySummary
#                 # date_key = timezone.now().astimezone(moscow_tz).date()
#                 # daily_summary, created = DailySummary.objects.get_or_create(user=request.user, date=date_key)
#                 # daily_summary.interval_count += 1
#                 # daily_summary.total_duration += interval.duration
#                 # daily_summary.save()
#
#             return redirect('time_interval_view')
#
#         elif 'reset' in request.POST:
#             # Удаляем все записи из модели TimeInterval для текущего пользователя
#             TimeInterval.objects.filter(user=request.user).delete()
#             return redirect('time_interval_view')
#
#     intervals = TimeInterval.objects.filter(user=request.user)
#     formatted_intervals = []
#
#     for interval in intervals:
#         if interval.start_time and interval.end_time:
#             duration = interval.duration
#             minutes, seconds = divmod(duration.total_seconds(), 60)
#             formatted_intervals.append({
#                 'start_time': interval.start_time.strftime("%H:%M:%S"),
#                 'end_time': interval.end_time.strftime("%H:%M:%S"),
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"})
#
#     daily_summary = DailySummary.objects.filter(user=request.user)
#     formatted_summary = []
#
#     for summary in daily_summary:
#         if summary.total_duration:
#             total_seconds = int(summary.total_duration.total_seconds())
#             hours, remainder = divmod(total_seconds, 3600)
#             minutes, seconds = divmod(remainder, 60)
#             formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
#         else:
#             formatted_duration = "00:00:00"
#
#         formatted_summary.append({
#             'date': summary.date,
#             'interval_count': summary.interval_count,
#             'total_duration': formatted_duration,
#         })
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summary': formatted_summary
#     })


from datetime import timedelta
import pytz
from django.utils import timezone
from django.shortcuts import redirect, render
from .models import TimeInterval, DailySummary

@authenticated_user_required
def time_interval_view(request):
    moscow_tz = pytz.timezone('Europe/Moscow')

    if request.method == 'POST':
        if 'start' in request.POST:
            # Записываем текущее московское время в start_time
            interval = TimeInterval(user=request.user, start_time=timezone.now().astimezone(moscow_tz).time())
            interval.save()
            return redirect('time_interval_view')

        elif 'stop' in request.POST:
            # Получаем последний интервал и записываем end_time
            interval = TimeInterval.objects.filter(user=request.user).last()
            if interval:
                interval.end_time = timezone.now().astimezone(moscow_tz).time()
                interval.save()

                # Обновляем DailySummary
                date_key = timezone.now().astimezone(moscow_tz).date()
                daily_summary, created = DailySummary.objects.get_or_create(user=request.user, date=date_key)
                daily_summary.interval_count += 1
                daily_summary.total_duration += interval.duration
                daily_summary.save()

            return redirect('time_interval_view')

        elif 'reset' in request.POST:
            # Удаляем все записи из модели TimeInterval для текущего пользователя
            TimeInterval.objects.filter(user=request.user).delete()
            return redirect('time_interval_view')

    intervals = TimeInterval.objects.filter(user=request.user)
    formatted_intervals = []

    for interval in intervals:
        if interval.start_time and interval.end_time:
            duration = interval.duration
            minutes, seconds = divmod(duration.total_seconds(), 60)
            formatted_intervals.append({
                'start_time': interval.start_time.strftime("%H:%M:%S"),
                'end_time': interval.end_time.strftime("%H:%M:%S"),
                'duration': f"{int(minutes)} мин {int(seconds)} сек"})

    daily_summary = DailySummary.objects.filter(user=request.user)
    formatted_summary = []

    for summary in daily_summary:
        if summary.total_duration:
            total_seconds = int(summary.total_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            formatted_duration = "00:00:00"

        formatted_summary.append({
            'date': summary.date,
            'interval_count': summary.interval_count,
            'total_duration': formatted_duration,
        })

    return render(request, 'time_interval.html', {
        'formatted_intervals': formatted_intervals,
        'daily_summary': formatted_summary
    })
