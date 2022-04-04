from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from typing import NewType
from django.contrib import messages
from .models import Food, Customer, Account, Order


# Create your views here.

def base(request):
    return render(request, 'Kiosk/base.html')

def hello_world(request):
    return render(request, 'Kiosk/test.html')

def view_order(request):
    order_objects = Order.objects.all()
    return render(request, 'Kiosk/view_order.html', {'orders':order_objects})

def view_order_details(request, pk):
    i = get_object_or_404(Order, pk=pk)
    return render(request, 'Kiosk/view_order_details.html', {'i':i})

def update_order(request, pk):
    if request.method=='POST':
        qty = request.POST.get('qty')
        payment_mode = request.POST.get('payment_mode')
        messages.success(request, 'Details updated.')
        Order.objects.filter(pk=pk).update(qty=qty,payment_mode=payment_mode)
        return redirect('view_order_details', pk=pk)
    else:
        i = get_object_or_404(Order, pk=pk)
        return render(request, 'Kiosk/update_order.html', {'i':i},)

def delete_order(request, pk):
    Order.objects.filter(pk=pk).delete()
    messages.success(request, 'Order deleted.')
    return redirect('view_order')

def view_food(request):
    food_objects = Food.objects.all()
    return render(request, 'Kiosk/view_food.html', {'foods':food_objects})

def view_food_details(request, pk):
    f = get_object_or_404(Food, pk=pk)
    return render(request, 'Kiosk/view_food_details.html', {'f': f})

def update_food_details(request, pk):
    if(request.method=='POST'):
        foodname = request.POST.get('name')
        foodname_match = Food.objects.filter(name=foodname).exclude(pk=pk)

        if len(foodname_match) > 0:
            messages.error(request, 'Food Item already exists')
            return redirect('update_food_details', pk=pk)
        else:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            created_at = request.POST.get('created_at')
            newdate = parse_datetime(created_at)

            green = True
            messages.success(request, 'Food Item Updated')

            Food.objects.filter(pk=pk).update(name=name, description=description, price=price, created_at=newdate)
            return redirect('view_food_details', pk=pk)
    else:
        f = get_object_or_404(Food, pk=pk)
        return render(request, 'Kiosk/update_food_details.html', {'f': f})

def delete_food(request, pk):
    Food.objects.filter(pk=pk).delete()
    messages.success(request, 'Food Item Deleted')
    return redirect('view_food')


def view_customer(request):
    customer_objects = Customer.objects.all()
    return render(request, 'Kiosk/view_customer.html', {'customers':customer_objects})

def login(request):
	if(request.method=="POST"):
		us = request.POST.get('user')
		pw = request.POST.get('pw')
		if Account.objects.filter(username=us, password=pw).exists() == True:
			return redirect('view_order')
		else:
			#return redirect('login')
			messages.error(request, 'Username/password is incorrect')
	return render(request, 'Kiosk/login.html')

def add_food(request):
    if(request.method=='POST'):
        foodname = request.POST.get('name')
        foodname_match = Food.objects.filter(name=foodname)

        if len(foodname_match) > 0:
            messages.error(request, 'Food Item already exists')
            return redirect('add_food')
        else:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            created_at = request.POST.get('created_at')

            Food.objects.create(name=name, description=description, price=price, created_at=created_at)
            messages.success(request, 'Food Item added successfully')
            return redirect('view_food')
    else:
        return render(request, 'Kiosk/add_food.html')

def add_customer(request):
    if(request.method=='POST'):
        customername = request.POST.get('name')
        customername_match = Customer.objects.filter(name=customername)

        if len(customername_match) > 0:
            messages.error(request, 'Customer name already exists')
            return redirect('add_customer')
        else:
            name = request.POST.get('name')
            address = request.POST.get('address')
            city = request.POST.get('city')

            Customer.objects.create(name=name, address=address, city=city)
            return redirect('view_customer')
    else:
        return render(request, 'Kiosk/add_customer.html')

def signup(request):
    if request.method == 'POST':
        us = request.POST.get('uname')
        pw = request.POST.get('pw')
        if Account.objects.filter(username=us).exists()==True:
            messages.error(request, "User already exists")
            return redirect('login')
        else:
            Account.objects.create(username=us, password=pw)
            messages.success(request, "Account created successfully")
            return redirect('login')
    return render(request, 'Kiosk/signup.html')

def view_customer_details(request, pk):
    c = get_object_or_404(Customer, pk=pk)
    return render(request, 'Kiosk/view_customer_details.html', {'c': c})

def update_customer_details(request, pk):
    if(request.method=='POST'):
        customername = request.POST.get('name')
        customername_match = Customer.objects.filter(name=customername).exclude(pk=pk)

        if len(customername_match) > 0:
            messages.error(request, 'Customer Name already exists!')
            return redirect('update_customer_details', pk=pk)
        else:
            name = request.POST.get('name')
            address = request.POST.get('address')
            city = request.POST.get('city')

            Customer.objects.filter(pk=pk).update(name=name, address=address, city=city)
            messages.success(request, 'Customer Details updated')
            return redirect('view_customer_details', pk=pk)
    else:
        c = get_object_or_404(Customer, pk=pk)
        return render(request, 'Kiosk/update_customer_details.html', {'c': c})

def delete_customer(request, pk):
    Customer.objects.filter(pk=pk).delete()
    messages.success(request, 'Customer Details Deleted')
    return redirect('view_customer')
