from datetime import time, timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.shortcuts import render, redirect
from .models import TimeInterval, DailySummary


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


# Без итогов
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
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#     })
# import pytz
# from django.utils import timezone
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import TimeInterval, DailySummary
#
#
# @authenticated_user_required
# def time_interval_view(request):
#     moscow_tz = pytz.timezone('Europe/Moscow')
#
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Проверяем, есть ли активный интервал
#             active_interval = TimeInterval.objects.filter(user=request.user, end_time__isnull=True).first()
#             if active_interval:
#                 messages.warning(request, "У вас уже есть активный интервал. Завершите его перед началом нового.")
#             else:
#                 messages.success(request, "Вы Нажали кнопку СТАРТ 'идет запись' ")
#                 # Создаем новый интервал только при нажатии "СТАРТ"
#                 interval = TimeInterval(user=request.user, start_time=timezone.now().astimezone(moscow_tz).time())
#                 interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний активный интервал и записываем end_time
#             interval = TimeInterval.objects.filter(user=request.user, end_time__isnull=True).last()
#             if interval:
#                 interval.end_time = timezone.now().astimezone(moscow_tz).time()
#                 interval.save()
#
#                 # Увеличиваем количество интервалов в DailySummary
#                 today = timezone.now().date()
#                 daily_summary, created = DailySummary.objects.get_or_create(user=request.user, date=today)
#                 daily_summary.interval_count += 1  # Увеличиваем количество интервалов на 1
#                 daily_summary.save()
#
#                 messages.success(request, "Интервал успешно завершен.")
#             else:
#                 messages.warning(request, "Нет активного интервала для завершения.")
#             return redirect('time_interval_view')
#
#         elif 'reset' in request.POST:
#             # Удаляем все записи из модели TimeInterval для текущего пользователя
#             TimeInterval.objects.filter(user=request.user).delete()
#             messages.success(request, "Все интервалы успешно сброшены.")
#             return redirect('time_interval_view')
#
#         elif 'delete_summary' in request.POST:
#             # Удаляем все записи из модели DailySummary для текущего пользователя
#             DailySummary.objects.filter(user=request.user).delete()
#             messages.success(request, "Все итоговые данные успешно удалены.")
#             return redirect('time_interval_view')
#
#     # Получение всех интервалов для текущего пользователя
#     intervals = TimeInterval.objects.filter(user=request.user)
#     formatted_intervals = []
#
#     total_duration = timezone.timedelta()  # Инициализация общей продолжительности
#     for interval in intervals:
#         if interval.start_time and interval.end_time:
#             duration = interval.duration  # Предполагается, что duration правильно вычисляется
#             total_duration += duration  # Суммируем продолжительность
#             minutes, seconds = divmod(duration.total_seconds(), 60)
#             formatted_intervals.append({
#                 'start_time': interval.start_time.strftime("%H:%M:%S"),
#                 'end_time': interval.end_time.strftime("%H:%M:%S"),
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     # Обновление или создание DailySummary
#     today = timezone.now().date()
#     daily_summary, created = DailySummary.objects.get_or_create(user=request.user, date=today)
#
#     # Обновление total_time
#     daily_summary.total_time = total_duration  # Устанавливаем общее время
#     daily_summary.interval_count = intervals.count()  # Устанавливаем количество интервалов
#     daily_summary.save()  # Сохраняем изменения
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summary': daily_summary,
#     })
#


import pytz
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TimeInterval, DailySummary


@authenticated_user_required
def time_interval_view(request):
    moscow_tz = pytz.timezone('Europe/Moscow')

    if request.method == 'POST':
        if 'start' in request.POST:
            # Проверяем, есть ли активный интервал
            active_interval = TimeInterval.objects.filter(user=request.user, end_time__isnull=True).first()
            if active_interval:
                messages.warning(request, "У вас уже есть активный интервал. Завершите его перед началом нового.")
            else:
                messages.success(request, "Вы Нажали кнопку СТАРТ 'идет запись' ")
                # Создаем новый интервал только при нажатии "СТАРТ"
                interval = TimeInterval(user=request.user, start_time=timezone.now().astimezone(moscow_tz).time())
                interval.save()
            return redirect('time_interval_view')

        elif 'stop' in request.POST:
            # Получаем последний активный интервал и записываем end_time
            interval = TimeInterval.objects.filter(user=request.user, end_time__isnull=True).last()
            if interval:
                interval.end_time = timezone.now().astimezone(moscow_tz).time()
                interval.save()

                # Увеличиваем количество интервалов в DailySummary
                today = timezone.now().date()
                daily_summary, created = DailySummary.objects.get_or_create(user=request.user, date=today)
                daily_summary.interval_count += 1  # Увеличиваем количество интервалов на 1
                daily_summary.save()

                messages.success(request, "Интервал успешно завершен.")
            else:
                messages.warning(request, "Нет активного интервала для завершения.")
            return redirect('time_interval_view')

        elif 'reset' in request.POST:
            # Удаляем все записи из модели TimeInterval для текущего пользователя
            TimeInterval.objects.filter(user=request.user).delete()
            messages.success(request, "Все интервалы успешно сброшены.")
            return redirect('time_interval_view')

        elif 'delete_summary' in request.POST:
            # Удаляем все записи из модели DailySummary для текущего пользователя
            DailySummary.objects.filter(user=request.user).delete()
            messages.success(request, "Все итоговые данные успешно удалены.")
            return redirect('time_interval_view')

        # Обработка значения current_seconds
        if 'current_seconds' in request.POST:
            current_seconds = int(request.POST['current_seconds'])
            # Здесь вы можете сохранить current_seconds в базе данных или использовать его по вашему усмотрению

    # Получение всех интервалов для текущего пользователя
    intervals = TimeInterval.objects.filter(user=request.user)
    formatted_intervals = []

    total_duration = timezone.timedelta()  # Инициализация общей продолжительности
    for interval in intervals:
        if interval.start_time and interval.end_time:
            duration = interval.duration  # Предполагается, что duration правильно вычисляется
            total_duration += duration  # Суммируем продолжительность
            minutes, seconds = divmod(duration.total_seconds(), 60)
            formatted_intervals.append({
                'start_time': interval.start_time.strftime("%H:%M:%S"),
                'end_time': interval.end_time.strftime("%H:%M:%S"),
                'duration': f"{int(minutes)} мин {int(seconds)} сек"
            })

    # Обновление или создание DailySummary
    today = timezone.now().date()
    daily_summary, created = DailySummary.objects.get_or_create(user=request.user, date=today)

    # Обновление total_time
    daily_summary.total_time = total_duration  # Устанавливаем общее время
    daily_summary.interval_count = intervals.count()  # Устанавливаем количество интервалов
    daily_summary.save()  # Сохраняем изменения

    return render(request, 'time_interval.html', {
        'formatted_intervals': formatted_intervals,
        'daily_summary': daily_summary,
    })
