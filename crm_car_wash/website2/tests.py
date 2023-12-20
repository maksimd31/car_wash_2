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

