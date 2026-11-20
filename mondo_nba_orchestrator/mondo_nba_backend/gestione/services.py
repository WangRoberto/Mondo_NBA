from typing import TYPE_CHECKING

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from users.models import User
else:
    User = get_user_model()
from django.db import transaction

from gestione.models import Cart, Comment, Product, UserPayment

# --- Product services ---


@transaction.atomic
def product_create(
    *,
    name: str,
    price: float,
    valuation: int = 0,
    category: str,
    description: str,
    image=None,
) -> Product:
    product = Product(
        name=name,
        price=price,
        valuation=valuation,
        category=category,
        description=description,
    )
    if image is not None:
        product.image = image
    product.full_clean()
    product.save()
    return product


@transaction.atomic
def product_update(
    *,
    product: Product,
    name: str | None = None,
    price: float | None = None,
    valuation: int | None = None,
    category: str | None = None,
    description: str | None = None,
    image=None,
) -> Product:
    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if valuation is not None:
        product.valuation = valuation
    if category is not None:
        product.category = category
    if description is not None:
        product.description = description
    if image is not None:
        product.image = image
    product.full_clean()
    product.save()
    return product


@transaction.atomic
def product_delete(*, product: Product) -> None:
    product.delete()


# --- Cart services ---


@transaction.atomic
def cart_add_product(
    *,
    user: User,
    product: Product,
    quantity: int = 1,
) -> Cart:
    cart, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        defaults={"quantity": quantity},
    )
    if not created:
        cart.quantity += quantity
        cart.save()
    return cart


@transaction.atomic
def cart_update_quantity(
    *,
    cart: Cart,
    quantity: int,
) -> Cart | None:
    if quantity <= 0:
        cart.delete()
        return None
    cart.quantity = quantity
    cart.save()
    return cart


@transaction.atomic
def cart_remove_product(*, cart: Cart) -> None:
    cart.delete()


# --- Comment services ---


@transaction.atomic
def comment_create(
    *,
    user: User,
    product: Product,
    content: str,
    valuation: int,
) -> Comment:
    comment = Comment(
        user=user,
        product=product,
        content=content,
        valuation=valuation,
    )
    comment.full_clean()
    comment.save()

    # Recalculate product valuation
    comments = Comment.objects.filter(product=product)
    total = sum(c.valuation for c in comments)
    product.valuation = round(total / comments.count()) if comments.count() > 0 else 0
    product.save()

    return comment


# --- Product services ---
# (existing product_create, product_update, product_delete above)

# --- Cart services ---
# (existing cart_add_product, cart_update_quantity, cart_remove_product above)

# --- Comment services ---
# (existing comment_create above)

# --- Payment services ---
# (existing payment_process_cart, payment_mark_completed above)


@transaction.atomic
def payment_mark_completed(*, stripe_checkout_id: str) -> UserPayment:
    payment = UserPayment.objects.get(stripe_checkout_id=stripe_checkout_id)
    payment.payment_bool = True
    payment.save()
    return payment


@transaction.atomic
def payment_process_cart(
    *,
    user: User,
    cart_ids: list,
    stripe_checkout_id: str,
    address: str,
) -> list:
    payments = []
    for cart_id in cart_ids:
        if not cart_id:
            continue
        cart = Cart.objects.get(id=cart_id)
        payment = UserPayment(
            user=user,
            product=cart.product,
            quantity=cart.quantity,
            stripe_checkout_id=stripe_checkout_id,
            address=address,
        )
        payment.save()
        cart.delete()
        payments.append(payment)
    return payments


# --- Stripe services ---


def stripe_checkout_create(
    *, cart_ids: list, country: str, city: str, address: str
) -> str:
    """Create a Stripe checkout session and return its URL."""
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": str(settings.PRODUCT_PRICE),
                "quantity": 1,
            }
        ],
        mode="payment",
        customer_creation="always",
        success_url=settings.REDIRECT_DOMAIN
        + "/gestione/payment_successful?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.REDIRECT_DOMAIN + "/gestione/payment_cancelled",
    )
    url = checkout_session.url
    if url is None:
        raise ValueError("Stripe checkout URL is None")
    return url


def payment_process_successful(
    *,
    user: User,
    stripe_checkout_id: str,
    cart_ids: list,
    country: str,
    city: str,
    address: str,
) -> list:
    """Process a successful payment: create UserPayment records and clear cart."""
    return payment_process_cart(
        user=user,
        cart_ids=cart_ids,
        stripe_checkout_id=stripe_checkout_id,
        address=f"{country} {city} {address}",
    )


# --- Admin product services ---


@transaction.atomic
def admin_product_create(
    *,
    image,
    name: str,
    price: float,
    valuation: int,
    category: str,
    description: str,
) -> Product:
    return product_create(
        name=name,
        price=price,
        valuation=valuation,
        category=category,
        description=description,
        image=image,
    )


@transaction.atomic
def admin_product_delete(*, product_id: int) -> None:
    product = Product.objects.get(id=product_id)
    product_delete(product=product)


@transaction.atomic
def admin_product_update_field(
    *,
    product_id: int,
    field: str,
    value,
) -> Product:
    product = Product.objects.get(id=product_id)
    setattr(product, field, value)
    product.full_clean()
    product.save()
    return product
