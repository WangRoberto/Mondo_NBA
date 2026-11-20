"""API URL routing for mondo_nba project."""
from django.urls import path

from gestione.api_views import (
    CartDetailAPIView,
    CartListCreateAPIView,
    CommentListCreateAPIView,
    LoginAPIView,
    PaymentListAPIView,
    ProductDetailAPIView,
    ProductListCreateAPIView,
    RegisterAPIView,
)

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name="auth-login"),
    path("auth/register/", RegisterAPIView.as_view(), name="auth-register"),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("comments/", CommentListCreateAPIView.as_view(), name="comment-list-create"),
    path("cart/", CartListCreateAPIView.as_view(), name="cart-list-create"),
    path("cart/<int:pk>/", CartDetailAPIView.as_view(), name="cart-detail"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]