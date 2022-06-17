from tabnanny import check
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("book/<int:book_id>/", views.book),
    path("shop/", views.shop),
    path("books/", views.books),
    path("book/preview/<int:book_id>/", views.preview),
    path("shop/book/<int:book_id>/", views.bookshop),
    path("addtocart/<int:book_id>/", views.addtocart),
    path("cart/", views.cart),
    path("removefromcart/<int:book_id>/", views.removefromcart),
    path("checkout/", views.checkout),
    path("address/<int:order_id>/", views.address),
    path("checkout-session/<int:order_id>/", views.checkout_session),
    path("session-success/", views.session_success),
    #path("/")
]