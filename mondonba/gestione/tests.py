from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.test import Client

# Create your tests here.
class testProduct(TestCase):

    def test_product_create(self):
        name = "Test"
        price = "10.0"
        image = "product-36.jpg"
        category = "Clothing"
        description = "Description"
        valuation = "0"

        Product.objects.create(name=name, price=price, image=image, category=category, description=description, valuation=valuation)
        product = Product.objects.get(name=name)

        self.assertIsNotNone(product)
        self.assertEqual(product.howManyEmptyStars(), range(0, 5))



    def test_view_shoppingCart(self):
        username = "test"
        email = "test@gmail.com"
        password = "prova12345"

        User.objects.create_user(username=username, email=email, password=password)

        c = Client()
        c.login(username="test", password="prova12345")

        response = c.get(reverse("gestione:shoppingCart"))
        self.assertEqual(response.status_code, 200, "Error")

        response = self.client.get(reverse("gestione:shoppingCart"))
        self.assertEqual(response.status_code, 302, "Error")

    def test_view_addCart(self):
        username = "test"
        email = "test@gmail.com"
        password = "prova12345"

        user = User.objects.create_user(username=username, email=email, password=password)

        c = Client()
        c.login(username="test", password="prova12345")

        response = c.get(reverse("gestione:product"))
        self.assertEqual(response.status_code, 200, "Error")

        name = "Vince Carter Funko Pop"
        product = Product.objects.get(name=name)

        response = c.get(reverse("gestione:productDetail", kwargs={'pk': product.id}))
        self.assertEqual(response.status_code, 200, "Error")

        data = {
            'num-product':1,
            'idProduct':product.id
        }

        response = c.post(reverse("gestione:addCart"), data, follow=True)
        self.assertEqual(response.status_code, 200, "Error")

        cart = Cart.objects.get(product=product, user=user)
        self.assertIsNotNone(cart, "Error")

        response = c.get(reverse("gestione:shoppingCart"))
        self.assertEqual(response.status_code, 200, "Error")




