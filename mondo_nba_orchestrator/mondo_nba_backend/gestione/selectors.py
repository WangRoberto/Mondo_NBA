
from django.contrib.auth.models import User

from gestione.models import Cart, Comment, Product, UserPayment

# --- Product selectors ---

def product_list(
    *,
    search: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    ordering: str | None = None,
) -> list:
    queryset = Product.objects.all()
    if search:
        queryset = queryset.filter(name__icontains=search)
    if category:
        queryset = queryset.filter(category=category)
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)
    if ordering:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by("-id")
    return list(queryset)


def product_get(*, product_id: int) -> Product:
    return Product.objects.get(id=product_id)


# --- Cart selectors ---

def cart_list_for_user(*, user: User) -> list:
    return list(Cart.objects.filter(user=user).select_related("product"))


# --- Comment selectors ---

def comments_for_product(*, product_id: int) -> list:
    return list(Comment.objects.filter(product_id=product_id).select_related("user"))


# --- Payment selectors ---

def user_payments(*, user: User) -> list:
    return list(UserPayment.objects.filter(user=user).select_related("product"))


def product_recommendations(
    *,
    product: Product,
    user: User,
    limit: int = 8,
) -> list[Product]:
    """Return recommended products based on purchase history and similarity."""
    recommended: list[Product] = []

    user_payment_products = UserPayment.objects.filter(product=product)
    for user_payment_product in user_payment_products:
        buyer = user_payment_product.user
        if buyer != user:
            other_payments = UserPayment.objects.filter(user=buyer).exclude(
                product=product
            )
            for other_payment in other_payments:
                other_product = other_payment.product
                if other_product is None:
                    continue
                if other_product not in recommended:
                    recommended.append(other_product)

    if len(recommended) < limit:
        price_products = Product.objects.filter(price=product.price).exclude(
            id=product.id
        )[: (limit - len(recommended))]
        for p in price_products:
            if p not in recommended:
                recommended.append(p)

    name_words = product.name.split()
    for word in name_words:
        if len(recommended) < limit:
            name_products = Product.objects.filter(name__icontains=word).exclude(
                id=product.id
            )[: (limit - len(recommended))]
            for p in name_products:
                if p not in recommended:
                    recommended.append(p)

    return recommended[:limit]
