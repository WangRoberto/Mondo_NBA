import time

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.list import ListView

from gestione.models import *
from gestione.selectors import product_recommendations
from gestione.services import (
    admin_product_create,
    admin_product_delete,
    admin_product_update_field,
    cart_add_product,
    cart_update_quantity,
    comment_create,
    payment_mark_completed,
    payment_process_successful,
    stripe_checkout_create,
)


# Create your views here.
class ProductListViewIndex(ListView):
    model = Product
    template_name = "index.html"
    ordering = ["-id"]  # noqa: RUF012

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            if self.request.session["show_login"]:
                self.request.session["show_login"] = False
                context["message"] = "Login with success!"
        except KeyError:
            print("Error!")

        return context


class ProductListView(ListView):
    model = Product
    template_name = "gestione/product.html"


class ProductOrder1(ListView):
    queryset = Product.objects.all().order_by("-valuation")
    template_name = "gestione/product.html"


class ProductOrder2(ListView):
    queryset = Product.objects.all().order_by("price")
    template_name = "gestione/product.html"


class ProductOrder3(ListView):
    queryset = Product.objects.all().order_by("-price")
    template_name = "gestione/product.html"


class ProductPrice1(ListView):
    queryset = (
        Product.objects.all().filter(price__gte=0, price__lte=50.0).order_by("price")
    )
    template_name = "gestione/product.html"


class ProductPrice2(ListView):
    queryset = (
        Product.objects.all().filter(price__gte=51, price__lte=100.0).order_by("price")
    )
    template_name = "gestione/product.html"


class ProductPrice3(ListView):
    queryset = (
        Product.objects.all().filter(price__gte=101, price__lte=150.0).order_by("price")
    )
    template_name = "gestione/product.html"


class ProductPrice4(ListView):
    queryset = (
        Product.objects.all().filter(price__gte=151, price__lte=200.0).order_by("price")
    )
    template_name = "gestione/product.html"


class ProductPrice5(ListView):
    queryset = Product.objects.all().filter(price__gte=201).order_by("price")
    template_name = "gestione/product.html"


class ListProductCart(ListView):
    template_name = "gestione/shoping-cart.html"

    def get_queryset(self):
        queryset = Cart.objects.all().filter(user=self.request.user)

        return queryset


class Search(ListView):
    # model = Product
    template_name = "gestione/product.html"
    # context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("search-product")

        return Product.objects.filter(name__icontains=query)


class ProductDetail(DetailView):
    model = Product
    template_name = "gestione/product-detail.html"
    # context_object_name = "product"

    """def get_queryset(self):
        query = self.request.GET.get('id')

        return Product.objects.filter(id=query)"""

    def get_context_data(self, *args, **kwargs):
        # Recupera il primary key del prodotto corrente dalla view
        pk = self.object.pk
        # Ottiene l'istanza del prodotto dal database tramite il suo ID
        tempProduct = Product.objects.get(id=pk)
        # Chiama il metodo della classe parent per ottenere il context base
        context = super().get_context_data(*args, **kwargs)

        # Sistema di raccomandazione prodotti (logica in selectors.py)
        context["products"] = product_recommendations(
            product=tempProduct, user=self.request.user
        )
        context["comments"] = Comment.objects.filter(product=pk)

        # Resetta i flag di sessione
        self.request.session["show"] = False
        self.request.session["show2"] = False
        context["error"] = False

        # Controlla se il login è avvenuto con successo
        try:
            if self.request.session["success"]:
                self.request.session["show"] = True
                self.request.session["success"] = False
        except KeyError:
            print("Error Cart!")

        # Controlla se il commento è stato aggiunto con successo
        try:
            if self.request.session["success2"]:
                self.request.session["show2"] = True
                self.request.session["success2"] = None

        except KeyError:
            print("Error Comment!")

        # Controlla se c'è un errore nel commento (utente ha già commentato)
        try:
            if self.request.session["success2"] == False:
                context["error"] = True

                tempUser = self.request.user
                tempProduct = Product.objects.get(id=pk)
                tempComment = Comment.objects.get(user=tempUser, product=tempProduct)
                if tempComment:
                    context["message"] = "You can only comment once per product!"
                self.request.session["success2"] = None
        except KeyError:
            print("Error2 Comment!")

        return context


@login_required
def addCart(request):

    if "num-product" in request.POST and "idProduct" in request.POST:
        numProducts = request.POST["num-product"]
        idProduct = request.POST["idProduct"]

        product = Product.objects.get(id=idProduct)
        cart_add_product(user=request.user, product=product, quantity=int(numProducts))

        request.session["success"] = True

        return redirect("gestione:productDetail", pk=idProduct)

    next = request.META.get("HTTP_REFERER")

    return HttpResponseRedirect(next)


@login_required
def updateCart(request):

    if "productsId" in request.POST and "contProducts" in request.POST:
        productsId = request.POST["productsId"]
        contProducts = request.POST["contProducts"]

        productsId = str(productsId).split("-")
        contProducts = str(contProducts).split("-")

        cont = 0
        for object in productsId:
            if object:
                try:
                    cart = Cart.objects.get(product=object, user=request.user.id)
                    qty = int(contProducts[cont])
                    cart_update_quantity(cart=cart, quantity=qty)
                except Cart.DoesNotExist:
                    pass
                cont = cont + 1

    return redirect("gestione:shoppingCart")


@login_required
def addComment(request):

    if (
        "review" in request.POST
        and "idProduct" in request.POST
        and "contStars" in request.POST
    ):
        review = request.POST["review"]
        idProduct = request.POST["idProduct"]
        contStars = request.POST["contStars"]
        tempUser = request.user
        tempProduct = Product.objects.get(id=idProduct)

        request.session["success2"] = False
        if int(contStars) > 0 or review:
            try:
                Comment.objects.get(user=tempUser, product=tempProduct)
            except Comment.DoesNotExist:
                comment_create(
                    user=tempUser,
                    product=tempProduct,
                    content=review,
                    valuation=int(contStars),
                )
                request.session["success2"] = True
            else:
                request.session["success2"] = False

    next = request.META.get("HTTP_REFERER")

    return HttpResponseRedirect(next)


class PurchasedProducts(ListView):
    template_name = "gestione/purchased-products.html"

    def get_queryset(self):
        queryset = UserPayment.objects.all().filter(user=self.request.user)

        return queryset


@login_required
def payment(request):

    if request.method == "POST":
        if (
            "cartId" in request.POST
            and "country" in request.POST
            and "city" in request.POST
            and "address" in request.POST
        ):
            request.session["payment"] = True
            request.session["cart_ids"] = request.POST["cartId"]
            request.session["country"] = request.POST["country"]
            request.session["city"] = request.POST["city"]
            request.session["address"] = request.POST["address"]

        cart_ids = str(request.session.get("cart_ids", "")).split("-")
        checkout_url = stripe_checkout_create(
            cart_ids=cart_ids,
            country=request.session.get("country", ""),
            city=request.session.get("city", ""),
            address=request.session.get("address", ""),
        )

        return redirect(checkout_url, code=303)

    return render(request, "gestione/purchased-products.html")


@login_required
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user = request.user
    message = ""
    try:
        if request.session["payment"]:
            request.session["payment"] = False
            if not request.session["payment"]:
                message = "Successful payment"

            tempCartIds = request.session["cart_ids"]
            cartIds = str(tempCartIds).split("-")

            payment_process_successful(
                user=user,
                stripe_checkout_id=checkout_session_id,
                cart_ids=cartIds,
                country=request.session.get("country", ""),
                city=request.session.get("city", ""),
                address=request.session.get("address", ""),
            )
    except KeyError:
        print("Error payment!")

    user_all_payments = UserPayment.objects.all().filter(user=user)

    return render(
        request,
        "gestione/purchased-products.html",
        {"customer": customer, "object_list": user_all_payments, "message": message},
    )


@login_required
def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST

    return render(request, "gestione/purchased-products.html")


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id", None)
        time.sleep(15)
        payment_mark_completed(stripe_checkout_id=session_id)

    return HttpResponse(status=200)


@login_required
def listProduct(request):

    if not request.user.is_staff:
        return redirect("/")
    page = 1
    if "page" in request.GET:
        page = request.GET["page"]

    object_list = Product.objects.all()[(5 * int(page) - 5) : (5 * int(page))]

    message = ""
    try:
        if request.session["action"]:
            request.session["action"] = False
            message = request.session["action_message"]
    except KeyError:
        print("Error to edit a product!")

    return render(
        request,
        "gestione/edit-product.html",
        {
            "object_list": object_list,
            "count": Product.objects.all().count(),
            "message": message,
        },
    )


@login_required()
def productAction(request):
    request.session["action"] = True
    message = ""
    if "action" in request.POST:
        action = str(request.POST["action"])
        message = "Success to " + action

        if action == "Create":
            if (
                "image" in request.FILES
                and "name" in request.POST
                and "price" in request.POST
                and "valuation" in request.POST
                and "category" in request.POST
                and "description" in request.POST
            ):
                admin_product_create(
                    image=request.FILES["image"],
                    name=request.POST["name"],
                    price=float(request.POST["price"]),
                    valuation=int(request.POST["valuation"]),
                    category=request.POST["category"],
                    description=request.POST["description"],
                )
        elif action == "Delete":
            if "deleteId" in request.POST:
                try:
                    admin_product_delete(product_id=int(request.POST["deleteId"]))
                except Exception:  # noqa: BLE001
                    message = "Error to deleting product!"
        else:
            if (
                "updateId" in request.POST
                and "whatField" in request.POST
                and ("field" in request.POST or "field" in request.FILES)
            ):
                id = request.POST["updateId"]
                whatField = request.POST["whatField"].lower()
                try:
                    field = request.POST["field"]
                except KeyError:
                    try:
                        field = request.FILES["field"]
                    except KeyError:
                        print("Field is not in FILES!")
                        field = None

                if field is not None:
                    try:
                        admin_product_update_field(
                            product_id=int(id),
                            field=whatField,
                            value=field,
                        )
                    except Exception:  # noqa: BLE001
                        message = "Error to update product!"

    request.session["action_message"] = message

    return redirect("gestione:edit_product")
