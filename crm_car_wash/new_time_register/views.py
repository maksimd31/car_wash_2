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
#     tm, created = Timer.objects.get_or_create(user=request.user)
#
#     if request.method == "POST":
#         if 'start' in request.POST:
#             tm.start_time = time.time()
#             tm.intervals = []
#             tm.save()
#         elif 'stop' in request.POST:
#             if tm.start_time:
#                 interval = time.time() - tm.start_time
#                 tm.elapsed_time += interval
#                 tm.intervals.append(interval)
#                 tm.start_time = None
#                 tm.save()
#
#     total_time = tm.elapsed_time + sum(tm.intervals)
#     return render(request, 'tim.html', {
#         'total_time': total_time,
#         'intervals': tm.intervals,
#     })

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Timer
# import time

# @login_required
# def timer_view(request):
#     timer, created = Timer.objects.get_or_create(user=request.user)
#
#     if request.method == "POST":
#         if 'start' in request.POST:
#             timer.start_time = time.time()
#             timer.intervals = []
#             timer.save()
#         elif 'stop' in request.POST:
#             if timer.start_time is not None:  # Проверка на наличие start_time
#                 interval = time.time() - timer.start_time
#                 timer.elapsed_time += interval
#                 timer.intervals.append(interval)
#                 timer.start_time = None
#                 timer.save()
#
#     total_time = timer.elapsed_time + sum(timer.intervals)
#     return render(request, 'tim.html', {
#         'total_time': total_time,
#         'intervals': timer.intervals,
#     })

#
# def timer_view(request):
#     tm, created = Timer.objects.get_or_create(user=request.user)
#
#     if request.method == "POST":
#         if 'start' in request.POST:
#             print("Start button pressed")  # Отладочное сообщение
#             tm.start_time = time.time()
#             tm.intervals = []
#             tm.save()
#         elif 'stop' in request.POST:
#             print("Stop button pressed")  # Отладочное сообщение
#             if tm.start_time:
#                 interval = time.time() - tm.start_time
#                 tm.elapsed_time += interval
#                 tm.intervals.append(interval)
#                 tm.start_time = None
#                 tm.save()
#
#     total_time = tm.elapsed_time + sum(tm.intervals)
#     return render(request, 'tim.html', {
#         'total_time': total_time,
#         'intervals': tm.intervals,
#     })
#
# def timer_view(request):
#     tm, created = Timer.objects.get_or_create(user=request.user)
#     print(f"Timer object: {tm}, created: {created}")  # Отладочное сообщение
#
#     if request.method == "POST":
#         print("POST request received")  # Отладочное сообщение
#         if 'start' in request.POST:
#             print("Start button pressed")  # Отладочное сообщение
#             tm.start_time = time.time()
#             tm.intervals = []
#             tm.save()
#             print("Timer started")  # Отладочное сообщение
#         elif 'stop' in request.POST:
#             print("Stop button pressed")  # Отладочное сообщение
#             if tm.start_time:
#                 interval = time.time() - tm.start_time
#                 tm.elapsed_time += interval
#                 tm.intervals.append(interval)
#                 tm.start_time = None
#                 tm.save()
#                 print("Timer stopped")  # Отладочное сообщение
#
#     total_time = tm.elapsed_time + sum(tm.intervals)
#     return render(request, 'tim.html', {
#         'total_time': total_time,
#         'intervals': tm.intervals,
#     })
#
# def timer_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             segment = TimeSegment(start_time=datetime.now())
#             segment.save()
#             request.session['segment_id'] = segment.id
#         elif 'stop' in request.POST:
#             segment_id = request.session.get('segment_id')
#             if segment_id:
#                 segment = TimeSegment.objects.get(id=segment_id)
#                 segment.end_time = datetime.now()  # Здесь используем timezone.now()
#                 segment.save()
#                 del request.session['segment_id']
#             return redirect('timer_view')
#
#     current_segment = TimeSegment.objects.filter(end_time__isnull=True).first()
#     return render(request, 'timer.html', {'current_segment': current_segment})
#
#
# from django.shortcuts import render, redirect
# from .models import TimeInterval
#
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             TimeInterval.objects.create(start_time=timezone.now())
#         elif 'stop' in request.POST:
#             interval = TimeInterval.objects.order_by('-id').first()
#             if interval and not interval.end_time:
#                 interval.end_time = timezone.now()
#                 interval.save()
#     intervals = TimeInterval.objects.all()
#     return render(request, 'time_interval.html', {'intervals': intervals})
#
# from django.shortcuts import render, redirect
# from .models import TimeInterval
# from .forms import TimeIntervalForm
# from django.utils import timezone
#
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time
#             interval = TimeInterval(start_time=timezone.now())
#             interval.save()
#             return redirect('time_interval_view')  # Перенаправляем на ту же страницу
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.last()
#             if interval:
#                 interval.end_time = timezone.now()
#                 interval.save()
#             return redirect('time_interval_view')  # Перенаправляем на ту же страницу
#
#     intervals = TimeInterval.objects.all()
#     form = TimeIntervalForm()
#     return render(request, 'time_interval.html', {'form': form, 'intervals': intervals})
# from django.shortcuts import render, redirect
# from .models import TimeInterval
# from django.utils import timezone
#
#
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time
#             interval = TimeInterval(start_time=timezone.now())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.last()
#             if interval:
#                 interval.end_time = timezone.now()
#                 interval.save()
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
#                 'start_time': interval.start_time,
#                 'end_time': interval.end_time,
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     return render(request, 'time_interval.html', {'formatted_intervals': formatted_intervals})

# from django.shortcuts import render, redirect
# from .models import TimeInterval
# from django.utils import timezone
#
#
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time
#             interval = TimeInterval(start_time=timezone.now())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.last()
#             if interval:
#                 interval.end_time = timezone.now()
#                 interval.save()
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
#                 'start_time': interval.start_time,
#                 'end_time': interval.end_time,
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     return render(request, 'time_interval.html', {'formatted_intervals': formatted_intervals})


# from django.shortcuts import render, redirect
# from .models import TimeInterval
# from django.utils import timezone
# from datetime import datetime
#
#
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time
#             interval = TimeInterval(start_time=timezone.now().time())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.last()
#             if interval:
#                 interval.end_time = timezone.now().time()
#                 interval.save()
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
#                 'start_time': interval.start_time,
#                 'end_time': interval.end_time,
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     return render(request, 'time_interval.html', {'formatted_intervals': formatted_intervals})

# from django.shortcuts import render, redirect
# from .models import TimeInterval
# from django.utils import timezone
# from datetime import datetime, timedelta
#
#
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time
#             interval = TimeInterval(start_time=timezone.now().time())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.last()
#             if interval:
#                 interval.end_time = timezone.now().time()
#                 interval.save()
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
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     # Группировка интервалов по дате
#     daily_summary = {}
#     for interval in intervals:
#         date_key = timezone.now().date()  # Используем текущую дату
#         if date_key not in daily_summary:
#             daily_summary[date_key] = {'count': 0, 'total_duration': timedelta()}
#
#         if interval.start_time and interval.end_time:
#             duration = interval.duration
#             daily_summary[date_key]['count'] += 1
#             daily_summary[date_key]['total_duration'] += duration
#
#     # Форматируем итоговое время
#     formatted_daily_summary = []
#     for date, summary in daily_summary.items():
#         total_seconds = int(summary['total_duration'].total_seconds())
#         hours, remainder = divmod(total_seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         formatted_daily_summary.append({
#             'date': date,
#             'count': summary['count'],
#             'total_duration': f"{hours:02}:{minutes:02}:{seconds:02}"
#         })
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summary': formatted_daily_summary
#     })
from django.shortcuts import render, redirect
from .models import TimeInterval, DailySummary
from django.utils import timezone
from datetime import datetime, timedelta


# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time
#             interval = TimeInterval(start_time=timezone.now().time())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.last()
#             if interval:
#                 interval.end_time = timezone.now().time()
#                 interval.save()
#
#                 # Обновляем DailySummary
#                 date_key = timezone.now().date()
#                 daily_summary, created = DailySummary.objects.get_or_create(date=date_key)
#                 daily_summary.interval_count += 1
#                 daily_summary.total_duration += interval.duration
#                 daily_summary.save()
#
#             return redirect('time_interval_view')
#
#         elif 'reset' in request.POST:
#             # Удаляем все записи из модели TimeInterval и DailySummary
#             TimeInterval.objects.all().delete()
#             DailySummary.objects.all().delete()
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
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     # Получаем сводные данные по дням
#     daily_summary = DailySummary.objects.all()
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summary': daily_summary
#     })

# @authenticated_user_required
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time
#             interval = TimeInterval(start_time=timezone.now().time())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал и записываем end_time
#             interval = TimeInterval.objects.last()
#             if interval:
#                 interval.end_time = timezone.now().time()
#                 interval.save()
#
#                 # Обновляем DailySummary
#                 date_key = timezone.now().date()
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
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     # Получаем сводные данные по дням
#     daily_summary = DailySummary.objects.all()
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summary': daily_summary
#     })


@authenticated_user_required
def time_interval_view(request):
    if request.method == 'POST':
        if 'start' in request.POST:
            # Записываем текущее время в start_time
            interval = TimeInterval(user=request.user, start_time=timezone.now().time())

            # interval = TimeInterval(start_time=timezone.now().time())
            interval.save()
            return redirect('time_interval_view')

        elif 'stop' in request.POST:
            # Получаем последний интервал и записываем end_time
            interval = TimeInterval.objects.filter(user=request.user).last()

            # interval = TimeInterval.objects.last()
            if interval:
                interval.end_time = timezone.now().time()
                interval.save()

                # Обновляем DailySummary
                date_key = timezone.now().date()
                daily_summary, created = DailySummary.objects.get_or_create(date=date_key)
                daily_summary.interval_count += 1
                daily_summary.total_duration += interval.duration
                daily_summary.save()

            return redirect('time_interval_view')

        elif 'reset' in request.POST:
            # Удаляем все записи из модели TimeInterval
            TimeInterval.objects.all().delete()
            return redirect('time_interval_view')

    intervals = TimeInterval.objects.all()
    formatted_intervals = []

    for interval in intervals:
        if interval.start_time and interval.end_time:
            duration = interval.duration
            minutes, seconds = divmod(duration.total_seconds(), 60)
            formatted_intervals.append({
                'start_time': interval.start_time.strftime("%H:%M:%S"),
                'end_time': interval.end_time.strftime("%H:%M:%S"),
                'duration': f"{int(minutes)} мин {int(seconds)} сек"
            })

    # Получаем сводные данные по дням
    daily_summary = DailySummary.objects.all()

    return render(request, 'time_interval.html', {
        'formatted_intervals': formatted_intervals,
        'daily_summary': daily_summary
    })

#
# from django.shortcuts import render, redirect
# from django.utils import timezone
# from .models import TimeInterval, DailySummary
#
# @authenticated_user_required
# def time_interval_view(request):
#     if request.method == 'POST':
#         if 'start' in request.POST:
#             # Записываем текущее время в start_time для текущего пользователя
#             interval = TimeInterval(user=request.user, start_time=timezone.now().time())
#             interval.save()
#             return redirect('time_interval_view')
#
#         elif 'stop' in request.POST:
#             # Получаем последний интервал для текущего пользователя и записываем end_time
#             interval = TimeInterval.objects.filter(user=request.user).last()
#             if interval:
#                 interval.end_time = timezone.now().time()
#                 interval.save()
#
#                 # Обновляем DailySummary для текущего пользователя
#                 date_key = timezone.now().date()
#
#                 # Попробуем получить существующую запись
#                 daily_summary = DailySummary.objects.filter(user=request.user, date=date_key).first()
#
#                 if daily_summary:
#                     # Если запись существует, обновляем её
#                     daily_summary.interval_count += 1
#                     daily_summary.total_duration += interval.duration
#                     daily_summary.save()
#                 else:
#                     # Если записи нет, создаем новую
#                     daily_summary = DailySummary(user=request.user, date=date_key, interval_count=1,
#                                                  total_duration=interval.duration)
#                     daily_summary.save()
#
#             return redirect('time_interval_view')
#
#         elif 'reset' in request.POST:
#             # Удаляем все записи из модели TimeInterval для текущего пользователя
#             TimeInterval.objects.filter(user=request.user).delete()
#             return redirect('time_interval_view')
#
#     # Получаем временные интервалы для текущего пользователя
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
#                 'duration': f"{int(minutes)} мин {int(seconds)} сек"
#             })
#
#     # Получаем сводные данные по дням для текущего пользователя
#     daily_summary = DailySummary.objects.filter(user=request.user)
#
#     return render(request, 'time_interval.html', {
#         'formatted_intervals': formatted_intervals,
#         'daily_summary': daily_summary
#     })