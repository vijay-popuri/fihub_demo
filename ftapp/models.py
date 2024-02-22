from django.db import models


class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.IntegerField(default=1)
	quantity = models.IntegerField(default=1)
	image = models.ImageField(upload_to='images/')
	desc = models.CharField(max_length=100)
	
class Customer(models.Model):
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	password = models.CharField(max_length=100)

class Cart(models.Model):
	cname = models.CharField(max_length=50)
	prod = models.CharField(max_length=50)
	prc = models.IntegerField(default=1)
	quan = models.IntegerField(default=1)
	img = models.ImageField(upload_to='images/')
	des = models.CharField(max_length=100)

class Order(models.Model):
	product = models.CharField(max_length=100)
	customer = models.CharField(max_length=100)
	quantity = models.IntegerField(default=1)
	phone = models.CharField(max_length=20, default='', blank=True)
	price = models.IntegerField(default=1)
	img1 = models.ImageField(upload_to='images/')
	des1 = models.CharField(max_length=100)
	