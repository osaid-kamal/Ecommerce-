from shop.models import Product
from django.shortcuts import render
from . models import Product,Order,Customer,OrderItem,Shipping
from math import ceil
from django.http import JsonResponse
from django.http import request
from .models import myuser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegForm,logged
from django.shortcuts import (get_object_or_404,HttpResponseRedirect)
from . import Checksum
import json
from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = 'mG!zKWiuh#H85&aX'



def index(request):
    products = Product.objects.all()
    print(products)
    allProd = []
    catprod = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslide = n//4+ceil((n/4)-(n//4))
        allProd.append([prod, range(1, nslide), nslide])
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    context={'items':items,'order':order}
    params = {'allProds': allProd,'cartItems':cartItems}
    return render(request, "shop/index.html", params)

def register(request):
    context = {}
    if request.POST:
        form = RegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get('password1')
            users = form.save()
            login(request, users)
            return redirect('login')
        else:
            context['registration_form'] = form

    else:
        form = RegForm()
        context['registration_form'] = form
    return render(request, 'shop/register.html', context)


@login_required(login_url="login")
def logoutas(request):
    logout(request)
    return redirect('/')


def loginas(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = logged(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
    else:
        form = logged()
    context['login_form'] = form
    return render(request, 'shop/login.html', context)
@login_required(login_url="loginas")
@csrf_exempt
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        
    else:
        items=[]
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'shop/cart.html',context)


@login_required(login_url="loginas")
@csrf_exempt
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('action',action)
    print("product:",productId)
    customer=request.user.customer
    product=Product.objects.get(productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        OrderItem.quantity=(OrderItem.quantity+1)
    elif action =='remove':
        OrderItem.quantity(OrderItem.quantity-1)

    OrderItem.save()
    if OrderItem.quantity<=0:
        OrderItem.delete()

    return JsonResponse("Item was added",safe=False)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    return render(request, "shop/contact.html")


def productView(request):
    return render(request, "shop/productView.html")


def tracker(request):
    return render(request, "shop/tracker.html")

@login_required(login_url="loginas")
@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        
    else:
        order={'get_cart_total':0,'get_cart_items':0}
        items=[]    
        par_dict={

            'MID': 'ltJQyd37007608829611',
            'ORDER_ID': str(order.t_id),
            'TXN_AMOUNT': str(order.get_cart_total),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlepayment/',

        }
   
        par_dict['CHECKSUMHASH'] = Checksum.generate_checksum(par_dict, MERCHANT_KEY)
        return  render(request, 'shop/paytm.html', {'par_dict': par_dict})
    context={'items':items,'order':order,'cartItems':cartItems,'shipping':False}
    return render(request, "shop/checkout.html",context)

def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def search(request):
    return render(request, "shop/search.html")
@csrf_exempt
def processOrder(request):
    print('Data',request.body)
    return JsonResponse('Payment complete',safe=False)
