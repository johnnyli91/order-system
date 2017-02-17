import json
import requests
from django.shortcuts import render, redirect
from ordersystem.settings import REVEL_HEADER


def index(request):
    return redirect('menu')


def get_menu(request):
    CATEGORY_URL = "https://api-playground.revelup.com/weborders/product_categories/?establishment=2"
    PRODUCT_URL = "https://api-playground.revelup.com/weborders/products/?establishment=2"

    category_response = requests.get(CATEGORY_URL, headers=REVEL_HEADER)
    category_data = category_response.json()
    product_response = requests.get(PRODUCT_URL, headers=REVEL_HEADER)
    product_data = product_response.json()

    menu = {"categories": category_data['data']}

    # Sort the products based on their id_category
    sorted_products = {}
    for product in product_data['data']:
        try:
            sorted_products[product['id_category']].append(product)
        except KeyError:
            sorted_products[product['id_category']] = [product]

    # Matches the sorted products with the corresponding categories
    for category in menu["categories"]:
        try:
            category['products'] = sorted_products[category['id']]
        except KeyError:
            category['products'] = []

    return render(request, "order/web_order_menu.html", menu)


def get_web_order_menu(request):
    API_URL = "https://api-playground.revelup.com/weborders/menu/?establishment=2"
    json_response = requests.get(API_URL, headers=REVEL_HEADER)
    response = json_response.json()
    data = response["data"]
    return render(request, "order/web_order_menu.html", data)


def calculate_total(request):
    API_URL = "https://api-playground.revelup.com/specialresources/cart/calculate/"
    raw_data = {"establishmentId": 2,
                "items": request.session['cart']}
    data = json.dumps(raw_data)
    json_response = requests.post(API_URL, headers=REVEL_HEADER, data=data)
    response = json_response.json()
    result = {"cart": request.session['cart'],
              "final_total": response['data']['final_total'],
              'subtotal': response['data']['subtotal'],
              'tax': response['data']['tax']}
    return render(request, "order/cart.html", result)


def add_to_cart(request):
    added_to_cart = False
    product_id = int(request.POST.get("product_id"))
    price = float(request.POST.get("price"))
    product_name = request.POST.get("product_name")

    if "cart" not in request.session:
        request.session["cart"] = []

    cart = request.session["cart"]

    for item in cart:
        if item["product"] == product_id:
            item["quantity"] += 1
            added_to_cart = True
    if not added_to_cart:
        cart.append({'price': price,
                     'product': product_id,
                     'product_name_override': product_name,
                     'quantity': 1})
    request.session["cart"] = cart
    return redirect("view_cart")


def remove_from_cart(request):
    product_id = int(request.POST.get("product_id"))
    cart = request.session["cart"]

    for item in cart:
        if item["product"] == product_id:
            item["quantity"] -= 1
            if item["quantity"] == 0:
                cart.remove(item)

    request.session["cart"] = cart
    return redirect("view_cart")


def view_cart(request):
    if "cart" not in request.session:
        request.session['cart'] = []
    data = {"cart": request.session['cart']}
    return render(request, "order/cart.html", data)


def clear_cart(request):
    request.session['cart'] = []
    return render(request, "order/cart.html")
