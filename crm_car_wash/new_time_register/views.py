from datetime import timezone
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
import pytz
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
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


# def add_manual_interval(user, start_time_str, end_time_str):
#     """Добавляет новый интервал вручную."""
#     moscow_tz = pytz.timezone('Europe/Moscow')
#
#     # Преобразуем строки времени в объекты времени
#     start_time = timezone.datetime.strptime(start_time_str, "%H:%M").time()
#     end_time = timezone.datetime.strptime(end_time_str, "%H:%M").time()
#
#     # Проверка, что время окончания позже времени начала
#     if end_time <= start_time:
#         raise ValueError("Время окончания должно быть позже времени начала.")
#
#     # Создаем новый интервал
#     interval = TimeInterval(user=user, start_time=start_time, end_time=end_time)
#     interval.save()
#
#     # Вычисляем продолжительность интервала
#     duration = timezone.datetime.combine(timezone.now().date(), end_time) - timezone.datetime.combine(
#         timezone.now().date(), start_time)
#     interval.duration = duration
#     interval.save()



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
#         elif 'add_manual_interval' in request.POST:
#             # Добавляем новый интервал вручную
#             start_time = request.POST.get('start_time')
#             end_time = request.POST.get('end_time')
#             add_manual_interval(request.user, start_time, end_time)
#             messages.success(request, "Новый интервал успешно добавлен.")
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
#     # Обнуляем interval_count и total_time для новой записи
#     daily_summary.interval_count = 0
#     daily_summary.total_time = timezone.timedelta()  # Обнуляем общее время
#     daily_summary.save()  # Сохраняем изменения
#
#     # Увеличиваем количество интервалов в DailySummary
#     daily_summary.interval_count += intervals.count()  # Устанавливаем количество интервалов
#     daily_summary.total_time += total_duration  # Устанавливаем общее время
#     daily_summary.save()  # Сохраняем изменения
#     # Получение всех итогов для текущего пользователя
#     daily_summaries = DailySummary.objects.filter(user=request.user).order_by('date')
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summaries': daily_summaries,  # Передаем все итоги
#     })
#



def add_manual_interval(user, start_time_str, end_time_str):
    """Добавляет новый интервал вручную."""
    moscow_tz = pytz.timezone('Europe/Moscow')

    # Преобразуем строки времени в объекты времени
    start_time = timezone.datetime.strptime(start_time_str, "%H:%M").time()
    end_time = timezone.datetime.strptime(end_time_str, "%H:%M").time()

    # Проверка, что время окончания позже времени начала
    if end_time <= start_time:
        raise ValueError("Время окончания должно быть позже времени начала.")

    # Создаем новый интервал
    interval = TimeInterval(user=user, start_time=start_time, end_time=end_time)
    interval.save()

    # Вычисляем продолжительность интервала
    duration = timezone.datetime.combine(timezone.now().date(), end_time) - timezone.datetime.combine(
        timezone.now().date(), start_time)
    interval.duration = duration
    interval.save()


@authenticated_user_required
def time_interval_view(request):
    moscow_tz = pytz.timezone('Europe/Moscow')

    if request.method == 'POST':
        if 'start' in request.POST:
            return handle_start_interval(request, moscow_tz)
        elif 'stop' in request.POST:
            return handle_stop_interval(request, moscow_tz)
        elif 'reset' in request.POST:
            return handle_reset_intervals(request)
        elif 'delete_summary' in request.POST:
            return handle_delete_summary(request)
        elif 'add_manual_interval' in request.POST:
            return handle_add_manual_interval(request)

    intervals = TimeInterval.objects.filter(user=request.user)
    formatted_intervals, total_duration = format_intervals(intervals)

    # Обновление или создание DailySummary
    update_daily_summary(request.user, intervals, total_duration)

    daily_summaries = DailySummary.objects.filter(user=request.user).order_by('date')

    return render(request, 'time_interval.html', {
        'formatted_intervals': formatted_intervals,
        'daily_summaries': daily_summaries,
    })


def handle_start_interval(request, moscow_tz):
    active_interval = TimeInterval.objects.filter(user=request.user, end_time__isnull=True).first()
    if active_interval:
        messages.warning(request, "У вас уже есть активный интервал. Завершите его перед началом нового.")
    else:
        messages.success(request, "Вы Нажали кнопку СТАРТ 'идет запись' \n Не забудьте нажать кнопку старт на секундомере")
        interval = TimeInterval(user=request.user, start_time=timezone.now().astimezone(moscow_tz).time())
        interval.save()
    return redirect('time_interval_view')


def handle_stop_interval(request, moscow_tz):
    interval = TimeInterval.objects.filter(user=request.user, end_time__isnull=True).last()
    if interval:
        interval.end_time = timezone.now().astimezone(moscow_tz).time()
        interval.save()
        messages.success(request, "Интервал успешно завершен.")
    else:
        messages.warning(request, "Нет активного интервала для завершения.")
    return redirect('time_interval_view')


def handle_reset_intervals(request):
    TimeInterval.objects.filter(user=request.user).delete()
    messages.success(request, "Все интервалы успешно сброшены.")
    return redirect('time_interval_view')


def handle_delete_summary(request):
    DailySummary.objects.filter(user=request.user).delete()
    messages.success(request, "Все итоговые данные успешно удалены.")
    return redirect('time_interval_view')


def handle_add_manual_interval(request):
    if request.method == 'POST' and 'add_manual_interval' in request.POST:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if start_time and end_time:
            try:
                add_manual_interval(request.user, start_time, end_time)
                messages.success(request, "Новый интервал успешно добавлен.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")
    return redirect('time_interval_view')


def format_intervals(intervals):
    formatted_intervals = []
    total_duration = timezone.timedelta()
    for interval in intervals:
        if interval.start_time and interval.end_time:
            duration = interval.duration
            total_duration += duration
            minutes, seconds = divmod(duration.total_seconds(), 60)
            formatted_intervals.append({
                'start_time': interval.start_time.strftime("%H:%M:%S"),
                'end_time': interval.end_time.strftime("%H:%M:%S"),
                'duration': f"{int(minutes)} мин {int(seconds)} сек"
            })
    return formatted_intervals, total_duration


def update_daily_summary(user, intervals, total_duration):
    today = timezone.now().date()
    daily_summary, created = DailySummary.objects.get_or_create(user=user, date=today)

    # Обнуляем interval_count и total_time для новой записи
    daily_summary.interval_count = 0
    daily_summary.total_time = timezone.timedelta()  # Обнуляем общее время
    daily_summary.save()  # Сохраняем изменения

    # Увеличиваем количество интервалов в DailySummary
    daily_summary.interval_count += intervals.count()  # Устанавливаем количество интервалов
    daily_summary.total_time += total_duration  # Устанавливаем общее время
    daily_summary.save()  # Сохраняем изменения


def intervals_for_date(request, date):
    date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
    # intervals = TimeInterval.objects.filter(date_create=date_obj)
    intervals = TimeInterval.objects.filter(user=request.user, date_create__date=date_obj)

    # intervals = TimeInterval.objects.filter(user=request.user)
    formatted_intervals, total_duration = format_intervals(intervals)

    # Обновление или создание DailySummary
    update_daily_summary(request.user, intervals, total_duration)

    # daily_summaries = DailySummary.objects.filter(user=request.user, date_create__date=date_obj)
    daily_summaries = DailySummary.objects.filter(user=request.user, date=date_obj)

    return render(request, 'your_template.html', {'intervals': intervals,'daily_summaries': daily_summaries,})
