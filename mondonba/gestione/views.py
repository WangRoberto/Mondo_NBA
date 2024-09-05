from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.conf import settings
import stripe
import time

from .models import *

# Create your views here.
class ProductListViewIndex(ListView):
    model = Product
    template_name = "index.html"
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListViewIndex, self).get_context_data(*args, **kwargs)
        try:
            if self.request.session["show_login"]:
                self.request.session["show_login"] = False
                context["message"] = "Login with success!"
        except:
            print("Error!")

        return context

class ProductListView(ListView):
    model = Product
    template_name = "gestione/product.html"

class ProductOrder1(ListView):
    queryset = Product.objects.all().order_by('-valuation')
    template_name = "gestione/product.html"

class ProductOrder2(ListView):
    queryset = Product.objects.all().order_by('price')
    template_name = "gestione/product.html"

class ProductOrder3(ListView):
    queryset = Product.objects.all().order_by('-price')
    template_name = "gestione/product.html"

class ProductPrice1(ListView):
    queryset = Product.objects.all().filter(price__gte=0, price__lte=50.0).order_by('price')
    template_name = "gestione/product.html"

class ProductPrice2(ListView):
    queryset = Product.objects.all().filter(price__gte=51, price__lte=100.0).order_by('price')
    template_name = "gestione/product.html"

class ProductPrice3(ListView):
    queryset = Product.objects.all().filter(price__gte=101, price__lte=150.0).order_by('price')
    template_name = "gestione/product.html"

class ProductPrice4(ListView):
    queryset = Product.objects.all().filter(price__gte=151, price__lte=200.0).order_by('price')
    template_name = "gestione/product.html"

class ProductPrice5(ListView):
    queryset = Product.objects.all().filter(price__gte=201).order_by('price')
    template_name = "gestione/product.html"

class ListProductCart (ListView):
    template_name = "gestione/shoping-cart.html"

    def get_queryset(self):
        queryset = Cart.objects.all().filter(user=self.request.user)
        return queryset

        """cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM gestione_cart GROUP BY product_id")
        result = cursor.fetchall()
        tempResult = []

        for i in result:
            tempResult.append(i[0])

        tempQuery = Cart.objects.raw('SELECT * FROM gestione_cart GROUP BY product_id')

        tempResult2 = []
        for i in tempQuery:
            tempResult3 = []
            tempResult3.append(i.user)
            tempResult3.append(i.product)
            tempResult2.append(tempResult3)

        res=list(zip(tempResult, tempResult2))
        return res"""

class Search(ListView):
    #model = Product
    template_name = "gestione/product.html"
    #context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("search-product")
        return Product.objects.filter(name__icontains=query)

class ProductDetail(DetailView):
    model = Product
    template_name = "gestione/product-detail.html"
    #context_object_name = "product"

    """def get_queryset(self):
        query = self.request.GET.get('id')
        return Product.objects.filter(id=query)"""

    def get_context_data(self, *args, **kwargs):
        pk = self.object.pk
        tempProduct = Product.objects.get(id=pk)
        context = super(ProductDetail, self).get_context_data(*args, **kwargs)

        # Raccomendation System
        listRaccomendationProducts = []

        # All payment that has that product
        tempUserPaymentProducts = UserPayment.objects.filter(product=tempProduct)
        for userPaymentProduct in tempUserPaymentProducts:

            # All user that bought that product
            tempUser = userPaymentProduct.user
            if tempUser != self.request.user:
                tempUserPaymentUsers = UserPayment.objects.filter(user=tempUser).exclude(product=tempProduct)

                # All other product that user bought
                for userPaymentUser in tempUserPaymentUsers:
                    tempProduct2 = userPaymentUser.product
                    listRaccomendationProducts.append(tempProduct2)

        if len(listRaccomendationProducts) < 8:

            tempProducts = Product.objects.filter(price=tempProduct.price)[:(8 - len(listRaccomendationProducts))]

            for p in tempProducts:
                if p not in listRaccomendationProducts and p != tempProduct:
                    listRaccomendationProducts.append(p)

        listName = (tempProduct.name).split()

        for name in listName:

            if len(listRaccomendationProducts) < 8:

                tempProducts = Product.objects.filter(name__icontains=name)[:(8 - len(listRaccomendationProducts))]

                for p in tempProducts:
                    if p not in listRaccomendationProducts and p != tempProduct:
                        listRaccomendationProducts.append(p)


        context['products'] = listRaccomendationProducts
        context['comments'] = Comment.objects.filter(product=pk)

        self.request.session["show"] = False
        self.request.session["show2"] = False
        context["error"] = False

        try:
            if self.request.session["success"]:
                self.request.session["show"] = True
                self.request.session["success"] = False
        except:
            print("Error Cart!")

        try:
            if self.request.session["success2"]:
                self.request.session["show2"] = True
                self.request.session["success2"] = None

        except:
            print("Error Comment!")

        try:
            if self.request.session["success2"] == False:
                context["error"] = True
                tempUser = self.request.user
                tempProduct = Product.objects.filter(id=pk)
                tempComment = Comment.objects.all().filter(user=tempUser, product=tempProduct)
                if tempComment:
                    context["message"] = "You can only comment once per product!"
                self.request.session["success2"] = None
        except:
            print("Error2 Comment!")


        return context
@login_required
def addCart(request):

    if "num-product" in request.POST and "idProduct" in request.POST:
        numProducts = request.POST["num-product"]
        idProduct = request.POST["idProduct"]
        #idUser = request.POST["idUser"]

        tempProduct = Product.objects.filter(id=idProduct)
        #tempUser = User.objects.filter(id=idUser)
        tempUser = request.user.id

        #for i in range(int(numProducts)):

        tempCart = Cart.objects.filter(product = idProduct, user = tempUser)

        if not tempCart:
            c = Cart()
            c.product = tempProduct[0]
            c.user = request.user
            c.quantity = numProducts
            c.save()
        else:
            tempCart[0].quantity = tempCart[0].quantity + int(numProducts)
            tempCart[0].save()

        request.session["success"] = True


        return redirect("gestione:productDetail", pk=idProduct)
    next = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(next)
@login_required
def updateCart(request):

    if "productsId" in request.POST and "contProducts" in request.POST:
        productsId = request.POST["productsId"]
        contProducts = request.POST["contProducts"]
        tempUser = request.user.id

        productsId = (str(productsId).split("-"))
        contProducts = (str(contProducts).split("-"))

        cont = 0
        for object in productsId:
            if object:
                if int(contProducts[cont]) == 0:
                    tempCart = Cart.objects.filter(product=object, user=tempUser)
                    tempCart[0].delete()
                else:
                    tempCart = Cart.objects.filter(product=object, user=tempUser).update(quantity=contProducts[cont])
                cont = cont + 1


    return redirect('gestione:shoppingCart')

@login_required
def addComment(request):

    if "review" in request.POST and "idProduct" in request.POST and "contStars" in request.POST:
        review = request.POST["review"]
        idProduct = request.POST["idProduct"]
        contStars = request.POST["contStars"]
        tempUser = request.user
        tempProduct = Product.objects.filter(id=idProduct)
        tempComment = Comment.objects.filter(user=tempUser, product=tempProduct[0])

        request.session["success2"] = False
        if (int(contStars) > 0 or review) and not tempComment:
            c = Comment()
            c.product = tempProduct[0]
            c.user = tempUser
            c.content = review
            c.valuation = contStars
            c.save()

            tempComment = Comment.objects.filter(product=tempProduct[0])

            cont = 0
            for comment in tempComment:
                cont = cont + comment.valuation

            cont = round(cont / tempComment.count())
            tempProduct.update(valuation=cont)

            request.session["success2"] = True


    next = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(next)

class PurchasedProducts(ListView):

    template_name = "gestione/purchased-products.html"

    def get_queryset(self):
        queryset = UserPayment.objects.all().filter(user=self.request.user)
        return queryset

@login_required
def payment(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        if "cartId" in request.POST and "country" in request.POST and "city" in request.POST and "address" in request.POST:
            request.session["payment"] = True
            request.session["cart_ids"] = request.POST["cartId"]
            request.session["country"] = request.POST["country"]
            request.session["city"] = request.POST["city"]
            request.session["address"] = request.POST["address"]
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                }
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = settings.REDIRECT_DOMAIN + '/gestione/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = settings.REDIRECT_DOMAIN + '/gestione/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'gestione/purchased-products.html')
@login_required
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
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
            cartIds = (str(tempCartIds).split("-"))
            for cartId in cartIds:
                if cartId:
                    user_payment = UserPayment()
                    user_payment.user = user
                    cart = Cart.objects.get(id=cartId)
                    user_payment.product = cart.product
                    user_payment.quantity = cart.quantity
                    user_payment.stripe_checkout_id = checkout_session_id
                    user_payment.address = request.session["country"] + " " + request.session["city"] + " " + request.session["address"]
                    user_payment.save()
                    cart.delete()

    except:
        print("Error payment!")

    user_all_payments = UserPayment.objects.all().filter(user=user)

    return render(request, 'gestione/purchased-products.html', {'customer':customer, 'object_list':user_all_payments, 'message': message})

@login_required
def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, 'gestione/purchased-products.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)


@login_required
def listProduct(request):

    if not request.user.is_staff:
        return redirect('/')
    page = 1
    if "page" in request.GET:
        page = request.GET["page"]

    object_list = Product.objects.all()[(5 * int(page) - 5):(5 * int(page))]

    message = ""
    try:
        if request.session["action"]:
            request.session["action"] = False
            message = request.session["action_message"]
    except:
        print("Error to edit a product!")


    return render(request, 'gestione/edit-product.html', {"object_list": object_list, "count": Product.objects.all().count(), "message": message})
@login_required()
def productAction(request):
    request.session["action"] = True
    message = ""
    if "action" in request.POST:

        action = str(request.POST["action"])
        message = "Success to " + action

        if action == "Create":
            if "image" in request.FILES and "name" in request.POST and "price" in request.POST and "valuation" in request.POST and "category" in request.POST and "description" in request.POST:
                image = request.FILES["image"]
                name = request.POST["name"]
                price = request.POST["price"]
                valuation = request.POST["valuation"]
                category = request.POST["category"]
                description = request.POST["description"]

                product = Product()
                product.image = image
                product.name = name
                product.price = price
                product.valuation = valuation
                product.category = category
                product.description = description
                product.save()
        elif action == "Delete":
            if "deleteId" in request.POST:

                id = request.POST["deleteId"]
                try:
                    Product.objects.get(id=id).delete()

                except:
                    message = "Error to deleting product!"
        else:
            if "updateId" in request.POST and "whatField" in request.POST and ("field" in request.POST or "field" in request.FILES):
                id = request.POST["updateId"]
                whatField = request.POST["whatField"].lower()
                try:
                    field = request.POST["field"]
                except:
                    print("Field is not in POST!")
                try:
                    field = request.FILES["field"]
                except:
                    print("Field is not in FILES!")

                try:
                    tempProduct = Product.objects.get(id=id)
                    setattr(tempProduct, whatField, field)
                    tempProduct.save()
                except:
                    message = "Error to update product!"

    request.session["action_message"] = message

    return redirect('gestione:edit_product')