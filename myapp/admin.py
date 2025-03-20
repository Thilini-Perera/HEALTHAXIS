from django.contrib import admin

from .models import Item, Order, OrderItem
from .models import MyModel
from .models import User
from .models import Customer

admin.site.register(Item)
admin.site.register(MyModel)
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
