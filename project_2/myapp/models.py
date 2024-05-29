from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_picture=models.ImageField(upload_to="profile_picture/")
	usertype=models.CharField(max_length=100,default="buyer")

	def __str__(self):
		return self.fname+" "+self.lname

class Product(models.Model):
	category=(("Men","Men"),
			  ("Women","Women"),
			  ("Kids","Kids"),
			  )
	
	size=(
		("s","s"),
		("M","M"),
		("L","L"),
		("XL","XL"),
		("XLL","XLL"),
		)
	color=(("Red","Red"),
		   ("White","White"),
		   ("Yellow","Yellow"),
		   ("Black","Black"),
		)
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_category=models.CharField(max_length=100,choices=category)
	product_name=models.CharField(max_length=100)
	product_desc=models.TextField()
	product_price=models.PositiveIntegerField()
	product_picture=models.ImageField(upload_to="Product_picture/")
	product_size=models.CharField(max_length=100,choices=size)
	product_color=models.CharField(max_length=100,choices=color)
	
	def __str__(self):
		return self.seller.fname+" "+self.product_name

class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.user.fname+" "+self.product.product_name

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	product_price=models.PositiveIntegerField()
	product_qty=models.PositiveIntegerField()
	total_price=models.PositiveIntegerField()
	payment_status=models.BooleanField(default=False)


	def __str__(self):
		return self.user.fname+" "+self.product.product_name
