"""
URL configuration for mondonba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import *
from .views import *

app_name = "gestione"

urlpatterns = [
    path("product/", ProductListView.as_view(), name="product"),
    path("product/order1", ProductOrder1.as_view(), name="productOrder1"),
    path("product/order2", ProductOrder2.as_view(), name="productOrder2"),
    path("product/order3", ProductOrder3.as_view(), name="productOrder3"),
    path("product/productprice1", ProductPrice1.as_view(), name="productPrice1"),
    path("product/productprice2", ProductPrice2.as_view(), name="productPrice2"),
    path("product/productprice3", ProductPrice3.as_view(), name="productPrice3"),
    path("product/productprice4", ProductPrice4.as_view(), name="productPrice4"),
    path("product/productprice5", ProductPrice5.as_view(), name="productPrice5"),
    path("product/q", Search.as_view(), name="search"),
    path("product/shoppingcart", login_required(ListProductCart.as_view()), name="shoppingCart"),
    path("product/detail/<int:pk>/", ProductDetail.as_view(), name="productDetail"),
    path("product/detail/addComment/", addComment, name="addComment"),
    path("product/detail/addcart", addCart, name="addCart"),
    path("product/detail/addcart/update/", updateCart, name="updateCart"),
    path("payment", payment, name="payment"),
    path("purchased_products/", login_required(PurchasedProducts.as_view()), name="purchased_products"),
    path("payment_successful", payment_successful, name="payment_successful"),
    path("payment_cancelled", payment_cancelled, name="payment_cancelled"),
    path("stripe_webhook", stripe_webhook, name="stripe_webhook"),
    path("edit_product/",  listProduct, name="edit_product"),
    path("edit_product/action", productAction, name="edit_product_action"),
]
