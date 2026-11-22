from django.db import models

class Customers(models. Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=10)
    address = models.TextField(max_length=100)

    def __str__(self):
        return self.username 

class Restaurants(models.Model):
    restaurent_name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    contact_number = models.CharField(max_length=15)
    cuisine_type = models.CharField(max_length=50)

    def __str__(self):
        return self.restaurent_name