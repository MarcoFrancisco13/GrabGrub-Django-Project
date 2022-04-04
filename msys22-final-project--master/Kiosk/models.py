from django.db import models
from datetime import datetime

class Food(models.Model):
    name = models.CharField(max_length = 300)
    description = models.CharField(max_length = 300)
    price = models.FloatField()
    created_at = models.DateTimeField(default=datetime.now)
    objects = models.Manager()

    def getName(self):
        return str(self.name)
    def getDesc(self):
        return str(self.description)
    def getPrice(self):
        return str(self.price)

    def __str__(self):
        return str(self.pk) + ": " + str(self.name) + " - " + str(self.price) + ", " + str(self.description) + " created at: " + str(self.created_at)

class Customer(models.Model):
    name = models.CharField(max_length = 300)
    address = models.CharField(max_length = 300)
    city = models.CharField(max_length = 300)
    objects = models.Manager()

    def getName(self):
        return str(self.name)
    def getAddress(self):
        return str(self.address)
    def getCity(self):
        return str(self.city)

    def __str__(self):
        return str(self.pk) + ": " + str(self.name) + " - " + str(self.address) + ", " + str(self.city)

class Account(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    objects = models.Manager()

    def getUsername(self):
        return self.username
    def getPassword(self):
        return self.password

    def __str__(self):
        return "Username, " + self.username + ", Password: " + self.password

class Order(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    qty = models.IntegerField(default='1')
    ordered_at = models.DateTimeField(default=datetime.now)
    cust_order = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length = 300, default='Cash', choices=[
        ('Cash', 'Cash'),
        ('Card', 'Card')])
    objects = models.Manager()

    def getMode(self):
        return str(self.payment_mode)
    def getQuantity(self):
        return str(self.qty)

    def __str__(self):
        return '{}: {} ({}). For {}: {}, {}. {}, ordered at {}'.format(
            self.pk,
            self.food.getName(),
            self.qty,
            self.cust_order.getName(),
            self.cust_order.getAddress(),
            self.cust_order.getCity(),
            self.payment_mode,
            self.ordered_at)