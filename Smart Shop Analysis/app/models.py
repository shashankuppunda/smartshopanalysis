from django.db import models
from django.contrib.auth.models import AbstractUser,User

from django.conf import settings
# Create your models here.
class User(AbstractUser): 
    phoneno = models.CharField(max_length=122,null=True,blank=True)
    name = models.CharField(max_length=122,null=True,blank=True)
    address = models.CharField(max_length=122,null=True,blank=True)
    is_admin = models.BooleanField("is_admin",default=False) 
    is_vendor = models.BooleanField("is_vendor",default=False) 
    is_customer = models.BooleanField("is_customer",default=False) 
    profile = models.ImageField(upload_to="profile/user_profile/")
    def save(self , *args , **kwargs): 
        if self.is_superuser and not self.is_admin: 
            self.is_admin = True 
        super().save(*args , **kwargs)
    def __str__(self):
        return self.name

class Product(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_products')
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='booked_products')
    product_name = models.CharField(max_length=255)
    mrp = models.DecimalField(max_digits=8, decimal_places=1)
    desc = models.CharField(max_length=200,null=True)
    product_image = models.ImageField(upload_to='images',blank=True,null=True)
    cerial_number = models.CharField(max_length=100)
    def __str__(self):
        return self.product_name

class Complaint(models.Model):
    complaint_by = models.CharField(max_length=40)
    complaint_mail = models.CharField(max_length=40)
    complaint_description = models.CharField(max_length=500)

    def __str__(self):
        return self.complaint_by

class SpecialOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    offer_name = models.CharField(max_length=255)
    vendor_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_specialoffer')
    def __str__(self):
        return self.offer_name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    prebook=models.BooleanField(default=False)

    def __str__(self):
        return f"Cart - Product: {self.product.product_name}, Added by: {self.added_by.username}"