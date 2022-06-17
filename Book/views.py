from importlib.metadata import metadata
from statistics import quantiles
from typing import Dict
from django.shortcuts import redirect, render
from gevent import idle
from matplotlib.axis import YAxis
from numpy import empty
from pyparsing import Or
from .models import Address, Book, Order, OrderItem
import stripe

def home(request):
    context = {"books" : Book.objects.all()}
    return render(request, "book/home.html", context)

def book(request, book_id):
    book = Book.objects.get(id = book_id)
    return render(request, "book/bookpage.html", {"book" : book})

def books(request):
    context = {"books" : Book.objects.all()}
    return render(request, "book/books.html", context)

def shop(request):
    context = {"books" : Book.objects.all()}
    return render(request, "book/shop.html", context)

def preview(request, book_id):
    book = Book.objects.get(id = book_id)
    return render(request, "book/preview.html", {"book" : book})

def bookshop(request, book_id):
    book = Book.objects.get(id = book_id)
    return render(request, "book/shopbook.html", {"book" : book})

def addtocart(request, book_id):
    cart = request.session.get("cart")
    # make sure cart exists
    if not cart:
        cart = {}
    quantity = request.POST.get("Quantity")
    if quantity == "":
        return redirect(f"/shop/book/{book_id}/")
    if str(book_id) in cart:
        cart[str(book_id)] = (int(quantity) + int(cart[str(book_id)]))
    else:
        cart[str(book_id)] = int(quantity)
    request.session["cart"] = cart
    print(request.session["cart"])
    return redirect(f"/shop/book/{book_id}/")

def removefromcart(request, book_id):
    cart = request.session.get("cart")
    # make sure cart exists
    if not cart:
        cart = {}
    cart.pop(str(book_id))
    request.session["cart"] = cart
    print(request.session["cart"])
    return redirect("/cart/")
    
def cart(request):
    cart = request.session.get("cart")
    if not cart:
        error = "cart.empty.error"
        return render(request, "book/cart.html", {"error" : error})
    items = []
    total = 0
    for id, quantity in cart.items():
        #id = key, quantity = value
        book = Book.objects.get(pk = id)
        cartitem = {
            "id" : id,
            "name" : book.name,
            "image" : book.image,
            "price" : book.price,
            "quantity" : quantity,
            "booktotal" : quantity * book.price
        }
        items.append(cartitem)
        total += quantity * book.price
    data = {"cart" : items, "total" : total}
    print(items)
    print(total)
    return render(request, "book/cart.html", data)

def checkout(request):
    cart = request.session.get("cart")
    if cart:
        order = Order()
        order.save()
        amount = 0
        for item, quan in cart.items():
            # item = Key
            # quan = Value
            book = Book.objects.get(pk = int(item))
            orderitem = OrderItem(order = order, book = book, quantity = quan)
            orderitem.save()
            amount += int(quan) * book.price
        order.amount = amount
        order.save()
        cart.clear()
        request.session["cart"] = cart
    return redirect(f"/address/{order.id}/")

def address(request, order_id):
    if request.method == "POST":
        data = request.POST
        print(data)

        email = data.get("email")
        contactnum = data.get("contactnum")

        order = Order.objects.get(id = order_id)
        order.emailid = email
        order.contactnum = contactnum
        order.save()

        firstname = data.get("firstname")
        lastname = data.get("lastname")
        country = data.get("country")
        postcode = data.get("postcode")
        city = data.get("city")
        state = data.get("state")

        address = Address(firstname = firstname, lastname = lastname, country = country, postcode = postcode, city = city, state = state)
        address.save()

        order.address = address
        order.save()

        return redirect(f"/checkout-session/{order_id}/")
    return render(request, "book/address.html", {"order": order_id})

def checkout_session(request, order_id):
    order = Order.objects.get(pk = order_id)
    stripe.api_key = "sk_test_51KeD1WDyHhdX3cQPmrSg2O9LDlwhbYeJzO6MYciqj3eULPspSNTx2m2PaZdVZ5K5TZbNgqANvWIqRg1LgETW1jOW00jpZ1hWxZ"
    session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            'currency': 'aud',
            'product_data': {
            'name': "Books",
            },
            'unit_amount': int(order.amount),
        },
        'quantity': 1,
        }],
        metadata = {
            "Order" : order.id
        },

        mode='payment',
        success_url='http://localhost:8000/session-success?session_id={CHECKOUT_SESSION_ID}/',
        cancel_url='http://localhost:8000/session-failure/',
    )
    return redirect(session.url)

def session_success(request):
    sid = request.GET['session_id']
    if sid[-1] == "/":
        sid = sid[:-1]
    print(sid)
    session = stripe.checkout.Session.retrieve(sid)
    order = Order.objects.get(pk = int(session.metadata["Order"]))
    order.status = "paid"
    order.save()
    return render(request, "book/success.html")