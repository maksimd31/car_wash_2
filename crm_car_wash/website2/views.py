import subprocess

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Order, Employee
from .forms import ClientForm, ClientUpdateForm, OrderForm, EmployeeForm, SignUpForm, AddRecordForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core import management


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
def delete_client(request):
    """
    Удаление пользователей
    :param request: ответ на запрос GET
    :return: render(request, 'delete_client.html')
    """
    if request.method == 'POST':
        license_plate = request.POST.get('license_plate')
        try:
            client = Client.objects.get(license_plate=license_plate)
            client.delete()
            return redirect('client_list')
        except Client.DoesNotExist:
            error_message = 'Клиент с указанным государственным номером не найден.'
            return render(request, 'delete_client.html', {'error_message': error_message})

    return render(request, 'delete_client.html')


# filename views.py
def update_client(request, license_plate):
    """
    Редактирование Пользователей
    :param request: ответ на запрос GET
    :param license_plate:
    :return: render(request, 'update_client.html'
    """
    client = get_object_or_404(Client, license_plate=license_plate)

    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', license_plate=license_plate)
    else:
        form = ClientUpdateForm(instance=client)

    return render(request, 'update_client.html', {'form': form, 'client': client})


# ORDER
# filename views.py
def create_order(request):
    """
    Создание заказа, сделки
    :param request: ответ на запрос GET
    :return: return render(request, 'create_order.html'
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})


# filename views.py
def delete_order(request, order_id):
    """
    Удаление заказа/сделки
    :param request: ответ на запрос GET
    :param order_id: идентификатор заказа/сделки
    :return: render(request, 'delete_order.html'
    """
    order = get_object_or_404(Order, pk=order_id)
    # Здесь мы используем функцию get_object_or_404,
    # чтобы получить объект модели Order по его первичному ключу (pk).
    # Если заказ с указанным order_id не существует, будет сгенерирована страница ошибки HTTP 404.
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    #     Здесь мы проверяем, был ли отправлен POST-запрос.
    #     Если это так, то мы удаляем заказ, вызывая метод delete() для объекта order.
    #     Затем мы перенаправляем пользователя на страницу, которая отображает список заказов
    #     (в данном случае с именем order_list).

    return render(request, 'delete_order.html', {'order': order})


# filename views.py
def update_order(request, order_id):
    """
    Редактирование заказа/сделки
    :param request: ответ на запрос GET
    :param order_id: идентификатор заказа/сделки
    :return: render(request, 'update_order.html'
    """
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)

    return render(request, 'update_order.html', {'form': form, 'order': order})


def order_list(request):
    """
    отображает список заказов (в данном случае с именем order_list).
    :param request:
    :return:  render(request, 'order_list.html'
    """
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


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
def add_employee(request):
    """
    Создание сотрудника
    :param request: ответ на запрос GET или POST
    :return: render 'add_employee.html' или перенаправление на страницу со списком сотрудников
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Перенаправление на страницу со списком сотрудников
    else:
        form = EmployeeForm()

    context = {'form': form}
    return render(request, 'add_employee.html', context)


def employee_list(request):
    """
    Отображение списка сотрудников
    :param request: ответ на запрос GET
    :return: render 'employee_list.html' с контекстом, содержащим список сотрудников
    """
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'employee_list.html', context)


def delete_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return render(request, 'delete_employee.html', {'employee': employee})


# # filename views.py
# def employee_list_del(request):
#     employees = Employee.objects.all()
#     return render(request, 'employee_list.html', {'employees': employees})

# # filename views.py
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Employee
# from .forms import EmployeeForm


def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form})


# Вот от сюда NEW

def home(request):
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли!")
            return redirect('home')
        else:
            messages.success(request, "ERROR ОШИБКА Please Try Again...")
            return redirect('home')
    else:
        # return render(request, 'homee.html', {'records': records})
        return render(request, 'home.html')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
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
    logout(request)
    messages.success(request, "Вы вышли из системы")
    return redirect('home')


@authenticated_user_required
def add_client(request):
    form = AddRecordForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            add_record = form.save()
            messages.success(request, "Запись добавлена...")
            return redirect('home')
    return render(request, 'add_client.html', {'form': form})


@authenticated_user_required
def client_home(request):
    clients = Client.objects.all()
    return render(request, 'client_home.html', {'clients': clients})


@authenticated_user_required
def customer_client(request, client_id):
    customer_client = Client.objects.get(id=client_id)
    return render(request, 'customer_client.html', {'customer_client': customer_client})


@authenticated_user_required
def delete_client(request, client_id):
    delete_it = Client.objects.get(id=client_id)
    delete_it.delete()
    messages.success(request, "Запись успешно удалена...")
    return redirect('client_home')


@authenticated_user_required
def update_client(request, client_id):
    current_record = Client.objects.get(id=client_id)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Запись Была Обновлена!")
        return redirect('client_home')
    return render(request, 'update_client.html', {'form': form})


def add_random_client(request):
    """
    Вызывает функцию из management/commands которая рандомно добавляет нового клиента
    :param request:
    :return:
    """
    # subprocess.call(['python', 'manage.py', 'add_random_client'])
    management.call_command('add_random_client')
    return redirect('client_home')


def del_random_client(request):
    management.call_command('delete_random_client')
    return redirect('client_home')


def update_random_client(reqwest):
    management.call_command('random_update_client')
    return redirect('client_home')
