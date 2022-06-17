from django.contrib import admin
from .models import Book, BookImage, BookStoryImage, Character, OrderItem, Order, Address

admin.site.register(Book)
admin.site.register(BookImage)
admin.site.register(BookStoryImage)
admin.site.register(Character)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)