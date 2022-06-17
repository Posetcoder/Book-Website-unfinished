from pyexpat import model
from typing import Mapping
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length = 50)
    #publisher = models.CharField(max_length=100, null = True, blank = True)
    short_desc = models.CharField(max_length=200, null = True, blank = True)
    long_desc = models.TextField()
    image = models.ImageField(null = True, blank = True)
    imageshop = models.ImageField(null = True, blank = True)
    externalBuy = models.URLField(null = True, blank = True)
    trailer = models.URLField(null = True, blank = True)
    price = models.FloatField(default = 0)
    
    #make a filter for roudning off if the decimals are only zero

    def __str__(self) -> str:
        return self.name

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.ImageField(null = True, blank = True)
    def __str__(self) -> str:
        return self.book.name

class BookStoryImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image1 = models.ImageField(null = True, blank = True)
    image2 = models.ImageField(null = True, blank = True)
    image3 = models.ImageField(null = True, blank = True)
    def __str__(self) -> str:
        return self.book.name

class Character(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null = True, blank = True)
    image = models.ImageField(null = True, blank = True)
    def __str__(self) -> str:
        return self.name + " - " + self.book.name

class Address(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.firstname + " " + self.lastname

class Order(models.Model):
    amount = models.FloatField(default = 0)
    status = models.CharField(max_length = 50, default = "created")
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    contactnum = models.CharField(max_length = 15, null = True, blank = True)
    emailid = models.EmailField(null=True,blank=True)
    paymentrefnum = models.CharField(max_length = 100, null = True, blank = True)
    def __str__(self) -> str:
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self) -> str:
        return str(self.order.id) + " "+ self.book.name