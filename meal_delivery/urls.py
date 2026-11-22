from django.contrib import admin
from django.urls import include, path
from meal_delivery import views

urlpatterns = [
    path('', views.home, name='home'),
    path('open_signup', views.open_signup, name='open_signup'),
    path('open_signin', views.open_signin, name='open_signin'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('open_add_new_restaurant', views.open_add_new_restaurant, name='open_add_new_restaurant'),
    path('add_new_restaurant', views.add_new_restaurant, name='add_new_restaurant'),
    path('open_show_restaurants', views.open_show_restaurants, name='open_show_restaurants'),
    path('show_restaurants', views.open_show_restaurants, name='show_restaurants'),
    path('open_update_restaurant', views.open_update_restaurant, name='open_update_restaurant'),
    path('update_restaurant', views.update_restaurant, name='update_restaurant')
]