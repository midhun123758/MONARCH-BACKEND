from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Product, Category

class ProductTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)  # <-- authenticate the client

        self.category1 = Category.objects.create(name='Category 1')
        self.product1 = Product.objects.create(
            name='Product 1',
            category=self.category1,
            price=100,
            stock=10
        )
        
    def test_products_by_category(self):
        url = reverse('category-products', kwargs={'pk': self.category1.id})
        response = self.client.get(url)  # authenticated client
        print(response.data)  # Debugging line to check the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], self.category1.name)
