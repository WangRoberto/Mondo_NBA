
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from gestione.models import Cart, Comment, Product
from gestione.selectors import (
    cart_list_for_user,
    comments_for_product,
    user_payments,
)
from gestione.serializers import (
    CartSerializer,
    CommentSerializer,
    ProductSerializer,
    UserPaymentSerializer,
)
from gestione.services import (
    cart_add_product,
    cart_remove_product,
    cart_update_quantity,
    comment_create,
    product_create,
    product_delete,
    product_update,
)

# --- Products ---

class ProductListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all().order_by("-id")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = product_create(**serializer.validated_data)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return Response(ProductSerializer(product).data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = product_update(product=product, **serializer.validated_data)
        return Response(ProductSerializer(updated).data)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_delete(product=product)
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Comments ---

class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        product_id = request.query_params.get("product")
        if product_id:
            comments = comments_for_product(product_id=int(product_id))
        else:
            comments = Comment.objects.all().order_by("-id")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.pop("product")
        product = get_object_or_404(Product, pk=product_id)
        comment = comment_create(
            user=request.user,
            product=product,
            content=serializer.validated_data["content"],
            valuation=serializer.validated_data.get("valuation", 3),
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


# --- Cart ---

class CartListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = cart_list_for_user(user=request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)
        product = get_object_or_404(Product, pk=product_id)
        cart = cart_add_product(user=request.user, product=product, quantity=quantity)
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Cart, pk=pk, user=user)

    def get(self, request, pk):
        cart = self.get_object(pk, request.user)
        return Response(CartSerializer(cart).data)

    def put(self, request, pk):
        cart = self.get_object(pk, request.user)
        quantity = request.data.get("quantity", cart.quantity)
        result = cart_update_quantity(cart=cart, quantity=quantity)
        if result is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(CartSerializer(result).data)

    def delete(self, request, pk):
        cart = self.get_object(pk, request.user)
        cart_remove_product(cart=cart)
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Payments ---

class PaymentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = user_payments(user=request.user)
        serializer = UserPaymentSerializer(payments, many=True)
        return Response(serializer.data)


# --- Auth ---

from django.contrib.auth.models import User
from rest_framework import status as drf_status
from rest_framework.authtoken.models import Token


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "Credenziali non valide"}, status=drf_status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email", "")
        password = request.data.get("password")
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username già in uso"}, status=drf_status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "username": user.username}, status=drf_status.HTTP_201_CREATED)
