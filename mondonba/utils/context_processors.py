from gestione.models import *
from django.contrib.auth.decorators import login_required
def getCart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.all().filter(user=request.user)
        return {"cart": cart}
    return {}
