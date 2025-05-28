# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
 

def index(request):
    table_numbers = range(1, 11)  # Numbers from 1 to 10
    return render(request, 'index.html', {
        "table_numbers": table_numbers,
    })


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')

        size_price = request.POST.get('size_price')
        if size_price:
            # For items with size and price combined
            try:
                size, price = size_price.split('-')
            except ValueError:
                return HttpResponse("Invalid size and price format.", status=400)
        else:
            # For fixed price items without size
            size = request.POST.get('item_size')  # optional, might be None
            price = request.POST.get('item_price')

            if not price:
                return HttpResponse("Price is required.", status=400)
            # If no size given, set to None or default
            if not size:
                size = "Regular"

        if not item_name:
            return HttpResponse("Item name is required.", status=400)

        # Initialize cart in session if not exists
        cart = request.session.get('cart', [])
        cart.append({
            'name': item_name,
            'size': size,
            'price': price
        })
        request.session['cart'] = cart

        return redirect('index')  # your home or menu page

    return HttpResponse("Invalid request method.", status=405)



    
def view_cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'cart.html', {"cart": cart})

def place_order(request):
    if request.method == "POST":
        cart = request.session.get('cart', [])
        table_no = request.POST.get('table_no')

        # Format order details from cart
        order_details = "\n".join([f"{item['name']} ({item.get('size', '')}) - ${item['price']}" for item in cart])

        # Create email message with table number
        message = f"Table Number: {table_no}\n\nOrder Details:\n{order_details}"

        send_mail(
            subject="New Order from Table " + str(table_no),
            message=message,
            from_email="Thoufic854@gmail.com",
            recipient_list=["Thoufic854@gmail.com"],
        )

        # Optionally clear cart and add success message
        request.session['cart'] = []
        messages.success(request, "Order placed successfully!")

        return redirect('index')  # or wherever you want to redirect after order

    else:
        return redirect('index')

@csrf_exempt  # or better, use @require_POST and CSRF properly
def remove_from_cart(request, item_index):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        try:
            cart.pop(int(item_index))
            request.session['cart'] = cart
        except (IndexError, ValueError):
            pass  # or handle error if needed
        return redirect('cart_view')  # use the correct URL name here

    return HttpResponse("Invalid request method.", status=405)


def set_table_number(request):
    if request.method == 'POST':
        table_no = request.POST.get('table_no')
        if table_no and table_no.isdigit():
            request.session['table_no'] = table_no  # Store in session
            return redirect('index')  # or wherever you want to redirect
        else:
            return HttpResponseBadRequest("Invalid table number.")
    return redirect('index')

def about_us(request):
    return render(request, 'about.html')