from django.contrib.sites import requests
from django.views.decorators.http import require_http_methods
from .models import Client
from .forms import SignUpForm, AddRecordClientForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core import management
import requests
from django.http import HttpResponseNotFound


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
            return redirect('home')

    return wrapper


def home(request):
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
            return redirect('home')
        else:
            messages.success(request, "ERROR ОШИБКА Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html')


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
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


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
    return redirect('home')


@authenticated_user_required
def add_client(request):
    """
       Добавляет нового клиента.

       Эта функция обрабатывает POST-запрос на добавление нового клиента.
       Если форма валидна, запись о новом клиенте добавляется в базу данных.
       После успешного добавления клиента, пользователь перенаправляется на главную страницу.

       Аргументы:
       request (HttpRequest): HTTP-запрос.

       Возвращает:
       HttpResponse: HTTP-ответ.
    """
    form = AddRecordClientForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            add_record = form.save()
            messages.success(request, "Запись добавлена")
            return redirect('client_home')
        else:
            messages.success(request, 'Ну удалось добавить запись')

    return render(request, 'add_client.html', {'form': form})


@authenticated_user_required
def client_home(request):
    """
        Получает из базы данных список всех клиентов и возвращает страницу 'client_home.html'.

        :param request: HTTP запрос.
        :return: HTTP ответ с отрендеренной страницей 'client_home.html' и контекстом, содержащим список клиентов.
    """
    clients = Client.objects.all()
    return render(request, 'client_home.html', {'clients': clients})


@authenticated_user_required
def customer_client(request, client_id):
    """
        Возвращает страницу с информацией о клиенте.

        :param request: Объект запроса
        :param client_id: идентификатор клиента
        :return: объект HttpResponse с отрендеренным шаблоном 'customer_client.html'
    """
    customer_client = Client.objects.get(id=client_id)
    return render(request, 'customer_client.html', {'customer_client': customer_client})


@authenticated_user_required
def delete_client(request, client_id):
    """Удаляет клиента из базы данных.

        Args:
            request (HttpRequest): Запрос от пользователя.
            client_id (int): Идентификатор клиента.

        Returns:
            HttpResponseRedirect: Перенаправление на страницу списка клиентов.
    """
    delete_it = Client.objects.get(id=client_id)
    delete_it.delete()
    messages.success(request, "Запись успешно удалена...")
    return redirect('client_home')


@authenticated_user_required
def update_client(request, client_id):
    """
       Обновляет информацию о клиенте.

       Параметры:
       - `request`: объект запроса HTTP
       - `client_id`: идентификатор клиента

       Возвращает:
       - `HttpResponse`: HTTP-ответ

       Исключения:
       - `Client.DoesNotExist`: если клиент с указанным `client_id` не существует

    """
    current_record = Client.objects.get(id=client_id)
    form = AddRecordClientForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Запись была обновлена!")
        return redirect('client_home')
    return render(request, 'update_client.html', {'form': form})


@authenticated_user_required
def add_random_client(request):
    """
    Вызывает функцию из management/commands которая рандомно добавляет нового клиента

    :param request: объект запроса
    :return: перенаправление на 'client_home'
    """
    # subprocess.call(['python', 'manage.py', 'add_random_client'])
    management.call_command('add_random_client')
    messages.success(request, "Добавлен случайный клиент!")
    return redirect('client_home')


@authenticated_user_required
def delete_random_client(request):
    """
    Вызывает функцию из management/commands которая рандомно удаляет клиента

    :param request: объект запроса
    :return: перенаправление на 'client_home'
    """
    management.call_command('delete_random_client')
    messages.success(request, "Удален случайный клиент!")
    return redirect('client_home')


@authenticated_user_required
def update_random_client(request):
    """
    Вызывает функцию из management/commands которая рандомно обновляет клиента

    :param request: объект запроса
    :return: перенаправление на 'client_home'
    """
    management.call_command('random_update_client')
    messages.success(request, "Отредактирован случайный клиент!")
    return redirect('client_home')


def get_weather(city):
    api_key = "ad71d819492af038206fc7075fea00fa"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"Текущая погода в {city} составляет {temperature}°C с {description}."
    else:
        return "Не удалось получить информацию о погоде."


def weather_view(request):
    if request.method == "POST":
        city = request.POST.get("city")

        if city:
            weather = get_weather(city)
            return render(request, "home.html", {"city": city, "weather": weather})

    return render(request, "home.html")


def delete_weather(request):
    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            return render(request, "home.html", {"city": city})

    return render(request, "home.html")


# def save_weather(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#
#         if city:
#             weather = get_weather(city)
#             with open("home.html", "a") as f:
#                 f.write(f"<p>{city}: {weather}</p>")
#
#     return render(request, "home.html")


@authenticated_user_required
def new_order(reqwest):
    """
    Скоро появится функционал
    :param reqwest:
    :return:
    """
    return render(reqwest, 'new_order.html')



@authenticated_user_required
def registr_time(reqwest):
    """
    Скоро появится функционал
    :param reqwest:
    :return:
    """
    return render(reqwest, 'registr_time.html')



@authenticated_user_required
# @require_http_methods(["GET"])
def search_clients(request):
    # Получаем параметр запроса 'q'
    query = request.GET.get('q')
    # Фильтруем объекты Client, где license_plate содержит query
    clients = Client.objects.filter(license_plate__icontains=query)
    if not clients:
        messages.success(request, 'Не найден номерной знак!')
        # return redirect('message.html')
    return render(request, 'client_home.html', {'clients': clients})


