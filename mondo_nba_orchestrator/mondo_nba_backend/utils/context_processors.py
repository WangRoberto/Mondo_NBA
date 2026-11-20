
from gestione.models import *


def getCart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.all().filter(user=request.user)
        return {"cart": cart}
    return {}
