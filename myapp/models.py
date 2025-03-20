from django.db import models
from django.contrib.auth.hashers import make_password

class Item(models.Model):
    item_id = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    expire_date = models.DateField()
    stocks = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class MyModel(models.Model):
    pharmacy_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)


class User(models.Model):
    id = models.AutoField(primary_key=True) 
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    pharmacy_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.username} - {self.pharmacy_name}"
    
class Customer(models.Model):
    uid = models.AutoField(primary_key=True) 
    uname = models.CharField(max_length=100)
    upassword = models.CharField(max_length=100)
    upharmacy_name = models.CharField(max_length=200)
    ucity = models.CharField(max_length=100)
    uaddress = models.CharField(max_length=200)
    uemail = models.EmailField(max_length=254)
    umobile_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.uname} - {self.upharmacy_name}"
       
class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.TextField(default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 

    def __str__(self):
        return f"Order {self.orderid} - {self.username}"

    def update_total(self):
        self.total = sum(item.total for item in self.order_items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)
        self.order.update_total() 

    def __str__(self):
        return f"{self.item_name} (Qty: {self.quantity})"
    
    class Meta:
        unique_together = ['order', 'item_name'] 