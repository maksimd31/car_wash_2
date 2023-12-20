from django.test import Client
from django.contrib.auth.models import User
from .models import Client as ClientModel

# User = get_user_model()
#
# class Car_wash_TestCases(TestCase):
#
#     def setUp(self) -> None:
#         self.user = User.object.creane(username='test', password='password')
#

from django.test import TestCase
from .models import Client, Order, Employee, City


class ClientModelTests(TestCase):
    def test_create_client(self):
        client = Client.objects.create(
            license_plate="123ABC",
            full_name="John Doe",
            phone_number="1234567890",
            email="johndoe@email.com",
            car_model="Test Model"
        )
        self.assertEqual(str(client), f"123ABC John Doe 1234567890 Test Model {client.created_at}")


# class TestViews(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.test_user = User.objects.create(username='testuser', password='testpassword')
#         self.test_client = ClientModel.objects.create(license_plate='123ABC', full_name='John Doe',
#                                                       phone_number='1234567890', email='johndoe@email.com',
#                                                       car_model='Test Model')
#
#     def test_add_client(self):
#         response = self.client.post('add_client', {
#             'license_plate': '456DEF',
#             'full_name': 'Jane Doe',
#             'phone_number': '0987654321',
#             'email': 'janedoe@email.com',
#             'car_model': 'Test Model 2'
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(ClientModel.objects.count(), 2)
#         self.assertEqual(ClientModel.objects.get(license_plate='456DEF').full_name, 'Jane Doe')

#     def setUp(self):
#         self.client = Client()
#         self.test_user = User.objects.create(username='testuser', password='testpassword')
#         self.test_client = ClientModel.objects.create(license_plate='123ABC', full_name='John Doe',
#                                                       phone_number='1234567890', email='johndoe@email.com',
#                                                       car_model='Test Model')
#
#     def test_authenticated_user_required(self):
#         resp = self.client.get('/add_client/')
#         self.assertEqual(resp.status_code, 302)

# def test_home_view(self):
#     resp = self.client.get('/')
#     self.assertEqual(resp.status_code, 200)
#
# def test_register_user_view(self):
#     resp = self.client.get('/register_user/')
#     self.assertEqual(resp.status_code, 200)
#
# def test_logout_user_view(self):
#     self.client.login(username='testuser', password='testpassword')
#     resp = self.client.get('/logout_user/')
#     self.assertEqual(resp.status_code, 302)
#
# def test_add_client_view(self):
#     self.client.login(username='testuser', password='testpassword')
#     resp = self.client.get('/add_client/')
#     self.assertEqual(resp.status_code, 200)
#
# def test_client_home_view(self):
#     self.client.login(username='testuser', password='testpassword')
#     resp = self.client.get('/client_home/')
#     self.assertEqual(resp.status_code, 200)
#
# def test_customer_client_view(self):
#     self.client.login(username='testuser', password='testpassword')
#     resp = self.client.get(f'/customer_client/{self.test_client.id}/')
#     self.assertEqual(resp.status_code, 200)
#
# def test_delete_client_view(self):
#     self.client.login(username='testuser', password='testpassword')
#     resp = self.client.get(f'/delete_client/{self.test_client.id}/')
#     self.assertEqual(resp.status_code, 302)
#
# def test_update_client_view(self):
#     self.client.login(username='testuser', password='testpassword')
#     resp = self.client.get(f'/update_client/{self.test_client.id}/')
#     self.assertEqual(resp.status_code, 200)
