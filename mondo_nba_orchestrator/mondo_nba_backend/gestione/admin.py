from django.contrib import admin

from gestione.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Comment)
admin.site.register(UserPayment)