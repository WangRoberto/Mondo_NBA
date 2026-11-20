from django.contrib.auth import get_user_model
from rest_framework import serializers

from gestione.models import Cart, Comment, Product, UserPayment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "valuation",
            "category",
            "description",
            "image",
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "product", "content", "valuation"]


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "product", "quantity"]


class UserPaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = UserPayment
        fields = [
            "id",
            "user",
            "product",
            "quantity",
            "payment_bool",
            "stripe_checkout_id",
            "address",
        ]
