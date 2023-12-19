from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Client, Order, Employee
from .forms import ClientForm, ClientUpdateForm, OrderForm, EmployeeForm, SignUpForm, AddRecordClientForm
from django.contrib.auth.models import User

# Create your tests here.
# User = get_user_model()
#
# class Car_wash_TestCases(TestCase):
#
#     def setUp(self) -> None:
#         self.user = User.object.creane(username='test', password='password')
#


class ClientTestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name='John Doe', email='john.doe@example.com', phone='1234567890')

    def test_client_creation(self):
        self.assertEqual(self.client.name, 'John Doe')
        self.assertEqual(self.client.email, 'john.doe@example.com')
        self.assertEqual(self.client.phone, '1234567890')

    def test_client_list_view(self):
        url = reverse('client_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_list.html')
        self.assertContains(response, self.client.name)
        self.assertContains(response, self.client.email)
        self.assertContains(response, self.client.phone)

    def test_add_client_view(self):
        url = reverse('add_client')
        data = {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'phone': '9876543210'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.count(), 2)
        new_client = Client.objects.get(name='Jane Smith')
        self.assertEqual(new_client.email, 'jane.smith@example.com')
        self.assertEqual(new_client.phone, '9876543210')

class OrderTestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name='John Doe', email='john.doe@example.com', phone='1234567890')
        self.order = Order.objects.create(client=self.client, title='Test Order', description='A test order')

    def test_order_creation(self):
        self.assertEqual(self.order.client, self.client)
        self.assertEqual(self.order.title, 'Test Order')
        self.assertEqual(self.order.description, 'A test order')

    def test_order_list_view(self):
        url = reverse('order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_list.html')
        self.assertContains(response, self.order.title)
        self.assertContains(response, self.order.description)

    def test_create_order_view(self):
        url = reverse('create_order')
        data = {'client': self.client.id, 'title': 'New Order', 'description': 'A new order'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 2)
        new_order = Order.objects.get(title='New Order')
        self.assertEqual(new_order.client, self.client)
        self.assertEqual(new_order.description, 'A new order')

class EmployeeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.employee = Employee.objects.create(user=self.user, name='John Doe', email='john.doe@example.com')

    def test_employee_creation(self):
        self.assertEqual(self.employee.user, self.user)
        self.assertEqual(self.employee.name, 'John Doe')
        self.assertEqual(self.employee.email, 'john.doe@example.com')

    def test_employee_list_view(self):
        url = reverse('employee_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_list.html')
        self.assertContains(response, self.employee.name)
        self.assertContains(response, self.employee.email)

    def test_add_employee_view(self):
        url = reverse('add_employee')
        data = {'user': self.user.id, 'name': 'Jane Smith', 'email': 'jane.smith@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Employee.objects.count(), 2)
        new_employee = Employee.objects.get(name='Jane Smith')
        self.assertEqual(new_employee.user, self.user)
        self.assertEqual(new_employee.email, 'jane.smith@example.com')
