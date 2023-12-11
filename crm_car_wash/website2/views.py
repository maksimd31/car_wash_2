import json
import subprocess
import urllib

from django.contrib.sites import requests
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Order, Employee, City
from .forms import ClientForm, ClientUpdateForm, OrderForm, EmployeeForm, SignUpForm, AddRecordForm, CityForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core import management

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import requests

# CLIENT
# filename views.py
# def add_client(request):
#     """
#     Создание клиента
#     :param request: ответ на запрос GET
#     :return: render 'add_client.html'
#     """
#     if request.method == 'POST':
#         form = ClientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('client_list')  # Перенаправление на страницу со списком клиентов
#     else:
#         form = ClientForm()
#
#     context = {'form': form}
#     return render(request, 'add_client.html', context)


# filename views.py
# def delete_client(request):
#     """
#     Удаление пользователей
#     :param request: ответ на запрос GET
#     :return: render(request, 'delete_client.html')
#     """
#     if request.method == 'POST':
#         license_plate = request.POST.get('license_plate')
#         try:
#             client = Client.objects.get(license_plate=license_plate)
#             client.delete()
#             return redirect('client_list')
#         except Client.DoesNotExist:
#             error_message = 'Клиент с указанным государственным номером не найден.'
#             return render(request, 'delete_client.html', {'error_message': error_message})
#
#     return render(request, 'delete_client.html')


# filename views.py
# def update_client(request, license_plate):
#     """
#     Редактирование Пользователей
#     :param request: ответ на запрос GET
#     :param license_plate:
#     :return: render(request, 'update_client.html'
#     """
#     client = get_object_or_404(Client, license_plate=license_plate)
#
#     if request.method == 'POST':
#         form = ClientUpdateForm(request.POST, instance=client)
#         if form.is_valid():
#             form.save()
#             return redirect('client_detail', license_plate=license_plate)
#     else:
#         form = ClientUpdateForm(instance=client)
#
#     return render(request, 'update_client.html', {'form': form, 'client': client})


# ORDER
# filename views.py
# def create_order(request):
#     """
#     Создание заказа, сделки
#     :param request: ответ на запрос GET
#     :return: return render(request, 'create_order.html'
#     """
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('order_list')
#     else:
#         form = OrderForm()
#     return render(request, 'create_order.html', {'form': form})


# filename views.py
# def delete_order(request, order_id):
#     """
#     Удаление заказа/сделки
#     :param request: ответ на запрос GET
#     :param order_id: идентификатор заказа/сделки
#     :return: render(request, 'delete_order.html'
#     """
#     order = get_object_or_404(Order, pk=order_id)
#     # Здесь мы используем функцию get_object_or_404,
#     # чтобы получить объект модели Order по его первичному ключу (pk).
#     # Если заказ с указанным order_id не существует, будет сгенерирована страница ошибки HTTP 404.
#     if request.method == 'POST':
#         order.delete()
#         return redirect('order_list')
#     #     Здесь мы проверяем, был ли отправлен POST-запрос.
#     #     Если это так, то мы удаляем заказ, вызывая метод delete() для объекта order.
#     #     Затем мы перенаправляем пользователя на страницу, которая отображает список заказов
#     #     (в данном случае с именем order_list).
#
#     return render(request, 'delete_order.html', {'order': order})


# filename views.py
# def update_order(request, order_id):
#     """
#     Редактирование заказа/сделки
#     :param request: ответ на запрос GET
#     :param order_id: идентификатор заказа/сделки
#     :return: render(request, 'update_order.html'
#     """
#     order = get_object_or_404(Order, pk=order_id)
#
#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('order_list')
#     else:
#         form = OrderForm(instance=order)
#
#     return render(request, 'update_order.html', {'form': form, 'order': order})


# def order_list(request):
#     """
#     отображает список заказов (в данном случае с именем order_list).
#     :param request:
#     :return:  render(request, 'order_list.html'
#     """
#     orders = Order.objects.all()
#     return render(request, 'order_list.html', {'orders': orders})


"""
Здесь мы определяем функции для каждой операции: create_order, delete_order, update_order и order_list.
- create_order: Создает новый заказ. Если запрос методом POST, то создается экземпляр формы (OrderForm) с данными из запроса и, если форма действительна, то сохраняется новый заказ в базу данных и происходит перенаправление на страницу списка заказов.
- delete_order: Удаляет существующий заказ. Если запрос методом POST, то заказ удаляется из базы данных и происходит перенаправление на страницу списка заказов.
- update_order: Редактирует существующий заказ. Если запрос методом POST, то создается экземпляр формы (OrderForm) с данными из запроса и, если форма действительна, то сохраняются изменения заказа в базе данных и происходит перенаправление на страницу списка заказов.
- order_list: Отображает список всех заказов.
Наконец, нужно создать соответствующие HTML-шаблоны для каждой из этих функций: create_order.html, delete_order.html, update_order.html и order_list.html, чтобы отображать формы и список заказов.
Также понадобится обновить файл urls.py, чтобы добавить соответствующие маршруты для этих функций.
"""


def authenticated_user_required(view_func):
    """
        Декоратор, требующий аутентификацию пользователя.

        Этот декоратор проверяет, является ли пользователь аутентифицированным.
        Если пользователь аутентифицирован, он вызывает исходную функцию представления.
        В противном случае он перенаправляет пользователя на домашнюю страницу с сообщением, что необходимо войти в систему.

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


def page_not_found(reqwest, exception):
    """
    Функция предоставления несуществующей страницы
    :param reqwest:
    :param exception:
    :return:
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# employee
# filename views.py
# def add_employee(request):
#     """
#     Создание сотрудника
#     :param request: ответ на запрос GET или POST
#     :return: render 'add_employee.html' или перенаправление на страницу со списком сотрудников
#     """
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')  # Перенаправление на страницу со списком сотрудников
#     else:
#         form = EmployeeForm()
#
#     context = {'form': form}
#     return render(request, 'add_employee.html', context)


# def employee_list(request):
#     """
#     Отображение списка сотрудников
#     :param request: ответ на запрос GET
#     :return: render 'employee_list.html' с контекстом, содержащим список сотрудников
#     """
#     employees = Employee.objects.all()
#     context = {'employees': employees}
#     return render(request, 'employee_list.html', context)

#
# def delete_employee(request, employee_id):
#     employee = Employee.objects.get(id=employee_id)
#
#     if request.method == 'POST':
#         employee.delete()
#         return redirect('employee_list')
#
#     return render(request, 'delete_employee.html', {'employee': employee})


# # filename views.py
# def employee_list_del(request):
#     employees = Employee.objects.all()
#     return render(request, 'employee_list.html', {'employees': employees})

# # filename views.py
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Employee
# from .forms import EmployeeForm

#
# def edit_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, instance=employee)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')
#     else:
#         form = EmployeeForm(instance=employee)
#
#     return render(request, 'edit_employee.html', {'form': form})
#

# Вот от сюда NEW

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
       После выхода, пользователю показывается сообщение об успешном выходе и
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
    form = AddRecordForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            add_record = form.save()
            messages.success(request, "Запись добавлена...")
            return redirect('home')
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

        :param request: объект запроса
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
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Запись Была Обновлена!")
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
    return redirect('client_home')


@authenticated_user_required
def delete_random_client(request):
    """
    Вызывает функцию из management/commands которая рандомно удаляет клиента

    :param request: объект запроса
    :return: перенаправление на 'client_home'
    """
    management.call_command('delete_random_client')
    return redirect('client_home')


@authenticated_user_required
def update_random_client(request):
    """
    Вызывает функцию из management/commands которая рандомно обновляет клиента

    :param request: объект запроса
    :return: перенаправление на 'client_home'
    """
    management.call_command('random_update_client')
    return redirect('client_home')


# @authenticated_user_required
# def weather_forecast():
#     management.call_command('temp')
#     return redirect('home')


# from django.shortcuts import render


# def weather(request):
#     city = "Toronto"
#     weather_condition = "Snow"
#     temperature = "-20°C"
#     time = "08:30 AM"
#     date = "Wednesday, 18 October 2019"
#     background_image_url = "<https://i.imgur.com/dpqZJV5.jpg>"
#
#     context = {
#         'city': city,
#         'weather_condition': weather_condition,
#         'temperature': temperature,
#         'time': time,
#         'date': date,
#         'background_image_url': background_image_url,
#     }
#
#     return render(request, 'weather.html', context)


# def index(request):
#     if request.method == 'POST':
#         city = request.POST['city']
#         ''' api key might be expired use your own api_key
#             place api_key in place of appid ="ad71d819492af038206fc7075fea00fa"  '''
#
#         # source contain JSON data from API
#
#         source = urllib.request.urlopen(
#             'http://api.openweathermap.org/data/2.5/weather?q ='
#             + city + '&appid = ad71d819492af038206fc7075fea00fa').read()
#
#         # converting JSON data to a dictionary
#         list_of_data = json.loads(source)
#
#         # data for variable list_of_data
#         data = {
#             "country_code": str(list_of_data['sys']['country']),
#             "coordinate": str(list_of_data['coord']['lon']) + ' '
#                           + str(list_of_data['coord']['lat']),
#             "temp": str(list_of_data['main']['temp']) + 'k',
#             "pressure": str(list_of_data['main']['pressure']),
#             "humidity": str(list_of_data['main']['humidity']),
#         }
#         print(data)
#     else:
#         data = {}
#     return render(request, "index.html", data)


# def index(request):
#     appid = 'ad71d819492af038206fc7075fea00fa'
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&&appid =' + appid
#
#     city = 'Moscow'
#     res = requests.get(url.format(city)).json()
#     city_info = {
#         'city': city,
#         'temp': res['main']['temp'],
#         'icon': res['weather'][0]['icon']
#
#     }
#     contex = {'info': city_info}
#
#     return render(request, 'index.html', contex)


# def index(request):
#     appid = 'ad71d819492af038206fc7075fea00fa'
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&&appid =' + appid
#
#     city = 'Moscow'
#     res = requests.get(url.format(city)).json()
#     city_info = {
#         'city': city,
#         'temp': res['main']['temp'],
#         'icon': res['weather'][0]['icon']
#
#     }
#     contex = {'info': city_info}
#
#     return render(request, 'index.html', contex)


# def get_weather(city):
#     api_key = "ad71d819492af038206fc7075fea00fa"
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         "appid": api_key,
#         "units": "metric"
#     }
#     response = requests.get(base_url, params=params)
#     data = response.json()
#
#     if data["cod"] == 200:
#         temperature = data["main"]["temp"]
#         description = data["weather"][0]["description"]
#         return f"Текущая погода в {city} составляет {temperature}°C с {description}."
#     else:
#         return "Не удалось получить информацию о погоде."
#
#
# def weather_view(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#
#         if city:
#             weather = get_weather("Москва")
#             return render(request, "weather.html", {"city": city, "weather": weather})
#
#     return render(request, "weather.html")


# def weather_view(request):
#     weather = get_weather("Москва")
#
#     return render(request, "weather.html", {"weather": weather})
#


# # Вариант3
# def get_weather(city):
#     api_key = "ad71d819492af038206fc7075fea00fa"
#     base_url = "<http://api.openweathermap.org/data/2.5/weather>"
#     params = {
#         "q": city,
#         "appid": api_key,
#         "units": "metric"
#     }
#     response = requests.get(base_url, params=params)
#     data = response.json()
#
#     if data["cod"] == 200:
#         temperature = data["main"]["temp"]
#         description = data["weather"][0]["description"]
#         return f"Текущая погода в {city} составляет {temperature}°C с {description}."
#     else:
#         return "Не удалось получить информацию о погоде."
#
#
# def weather_view(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#
#         if city:
#             weather = get_weather(city)
#             return render(request, "weather.html", {"city": city, "weather": weather})
#
#     return render(request, "weather.html")

# # Варинт 4
# # views.py
# def get_weather(city):
#     api_key = "ad71d819492af038206fc7075fea00fa"
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         "appid": api_key,
#         "units": "metric"
#     }
#     response = requests.get(base_url, params=params)
#     data = response.json()
#
#     if data["cod"] == 200:
#         temperature = data["main"]["temp"]
#         description = data["weather"][0]["description"]
#         return f"Текущая погода в {city} составляет {temperature}°C с {description}."
#     else:
#         return "Не удалось получить информацию о погоде."
#
#
# def weather_view(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#
#         if city:
#             weather = get_weather(city)
#             return render(request, "home.html", {"city": city, "weather": weather})
#
#     return render(request, "home.html")
#
#
# def delete_weather(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#         if city:
#             return render(request, "home.html", {"city": city})
#
#     return render(request, "home.html")
#
# # ВАРИНТ5
# # views.py
# def get_weather(city):
#     api_key = "ad71d819492af038206fc7075fea00fa"
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         "appid": api_key,
#         "units": "metric"
#     }
#     response = requests.get(base_url, params=params)
#     data = response.json()
#
#     if data["cod"] == 200:
#         temperature = data["main"]["temp"]
#         description = data["weather"][0]["description"]
#         return f"Текущая погода в {city} составляет {temperature}°C с {description}."
#     else:
#         return "Не удалось получить информацию о погоде."
#
#
# def weather_view(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#
#         if city:
#             weather = get_weather(city)
#             return render(request, "home.html", {"city": city, "weather": weather})
#
#     return render(request, "home.html")
#
#
# def delete_weather(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#         if city:
#             return render(request, "home.html", {"city": city})
#
#     return render(request, "home.html")
#
#
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

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
    city = 'London'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)

def new_order(reqwest):
    return render(reqwest, 'new_order.html')
