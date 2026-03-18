from datetime import timedelta
from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from orders.models import Order
from products.models import Product


class OrderCreateApiTests(APITestCase):
    def setUp(self):
        self.url = reverse("order-me-list")
        self.user = User.objects.create_user(
            email="buyer@example.com",
            password="strong-pass-123",
            first_name="Test",
            last_name="Buyer",
            birthdate=timezone.localdate() - timedelta(days=1),
        )
        self.user.welcome_discount = 10
        self.user.save(update_fields=["welcome_discount"])
        self.product = Product.objects.create(
            name="Case A",
            price=Decimal("100.00"),
        )

    def test_create_order_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "city": "Bishkek",
            "address": "Main street 1",
            "phone_number": "+996700000000",
            "order_items": [
                {
                    "product": self.product.id,
                    "quantity": 2,
                }
            ],
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.city, "Bishkek")
        self.assertEqual(order.address, "Main street 1")
        self.assertEqual(order.phone_number, "+996700000000")
        self.assertEqual(order.total_price, Decimal("180.00"))
        self.assertEqual(order.discount, Decimal("20.00"))
        self.assertEqual(order.welcome_discount, 10)

        self.assertEqual(order.order_items.count(), 1)
        item = order.order_items.first()
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, Decimal("200.00"))

    def test_create_order_requires_authentication(self):
        payload = {
            "order_items": [
                {
                    "product": self.product.id,
                    "quantity": 1,
                }
            ],
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_without_items_returns_400(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "city": "Bishkek",
            "address": "Main street 1",
            "phone_number": "+996700000000",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
