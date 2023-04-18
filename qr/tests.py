from django.test import TestCase
import unittest
from django.test import Client
from django.urls import reverse
from PIL import Image
from .models import *
# Create your tests here.

class QRConvertTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_qr_conversion(self):
        # Create a sample product instance
        product_data = {
            'title': 'Test Product',
            'description': 'This is a test product',
        }
        response = self.client.post(reverse('index'), data=product_data)
        self.assertEqual(response.status_code, 302)

        # Check that the product has a QR code
        product = Post.objects.get(title='Test Product')
        self.assertIsNotNone(product.qr_code)

        # Check that the QR code is a valid image
        qr_code_file = product.qr_code
        with qr_code_file.open() as f:
            image = Image.open(f)
            self.assertEqual(image.format, 'PNG')