from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, default=None)
    price = models.FloatField(default=0.0)
    valuation = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="products/", default="no-image.jpg", blank=True)

    def __str__(self):
        return ("Name:" + self.name + "\n" +
                "Price:" + str(self.price) + "\n" +
                "Valuation:" + str(self.valuation) + "\n" +
                "Category:" + self.category + "\n" +
                "Description:" + self.description + "\n"
                )

    def howManyStars(self):
        return range(self.valuation)

    def howManyEmptyStars(self):
        return range(5 - self.valuation)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cartUser")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartProduct")
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return ("\n:" + "User:" + str(self.user) + "\n" +
                "Product:" + str(self.product) +
                "Quantity:" + str(self.quantity)
                )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentUser")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="commentProduct")
    content = models.CharField(max_length=1000)
    valuation = models.IntegerField(default=3)

    def __str__(self):
        return ("User:" + str(self.user) + "\n" +
                "Product:" + str(self.product) + "\n" +
                "Content:" + str(self.content) + "\n" +
                "Valuation:" + str(self.valuation) + "\n"
                )

    def howManyStars(self):
        return range(self.valuation)

    def howManyEmptyStars(self):
        return range(5 - self.valuation)

class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userPaymentId")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="userPaymentProduct")
    quantity = models.IntegerField(default=0)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    address = models.CharField(max_length=500)

    def __str__(self):
        return ("User:" + str(self.user) + "\n" +
                "Product:" + str(self.product) + "\n" +
                "Quantity:" + str(self.quantity) + "\n" +
                "payment_bool:" + str(self.payment_bool) + "\n" +
                "stripe_checkout_id:" + str(self.stripe_checkout_id) + "\n"
                "address:" + str(self.address)
                )

