from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from .models import Customers, Restaurants

def home(request):
    return render(request, 'index.html')

def open_signup(request):
    return render(request, 'signup.html')

def open_signin(request):
    return render(request, 'signin.html')

@staff_member_required
def admin_home(request):
    return render(request, 'admin_home.html')

def signup(request):
    if request.method != 'POST':
        return render(request, 'signup.html')

    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    mobile = request.POST.get('mobile', '').strip()
    address = request.POST.get('address', '').strip()

    if Customers.objects.filter(username=username).exists():
        return render(request, 'signup.html', {
            'error': 'Username already exists. Please choose a different username.'
        })

    try:
        Customers.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            mobile=mobile,
            address=address,
        )
    except IntegrityError:
        return render(request, 'signup.html', {
            'error': 'An account with this email already exists.'
        })

    return redirect('open_signin')

def signin(request):
    if request.method != 'POST':
        return render(request, 'signin.html')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_staff:
        auth_login(request, user)
        return redirect('admin_home')

    customer = Customers.objects.filter(username=username).first()

    if customer is None or not (
        check_password(password, customer.password) or customer.password == password
    ):
        return render(request, 'signin.html', {
            'error': 'Invalid username or password.'
        })

    if customer.password == password:
        customer.password = make_password(password)
        customer.save(update_fields=['password'])

    request.session['customer_id'] = customer.pk
    return redirect('home')

def open_add_new_restaurant(request):
    return render(request, 'add_new_restaurant.html')

def add_new_restaurant(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name', '').strip()
        restaurant_address = request.POST.get('restaurant_address', '').strip()
        cuisine_type = request.POST.get('cuisine_type', '').strip()
        image = request.FILES.get('image')
        rating = request.POST.get('rating', '').strip()

        try:
            Restaurants.objects.get(restaurent_name = restaurant_name)
            return HttpResponse("Restaurant with this name already exists.")
        except:
            Restaurants.objects.create(
                restaurent_name=restaurant_name,
                address=restaurant_address,
                image=image,
                cuisine_type=cuisine_type,
                rating=rating
            )
        return redirect('show_restaurants')

    return render(request, 'add_new_restaurant.html')

def open_show_restaurants(request):
    restaurants = Restaurants.objects.all()
    return render(request, 'show_restaurants.html', {'restaurants': restaurants})

def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurants.objects.get(id=restaurant_id)
    return render(request, 'update_restaurant.html', {'restaurant': restaurant})    

