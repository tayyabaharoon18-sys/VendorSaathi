from django.db import models
from django.contrib.auth.models import User

class VendorProfile(models.Model):
    CATEGORY_CHOICES = [
        ('Food & Beverages', 'Food & Beverages'),
        ('Fashion & Tailoring', 'Fashion & Tailoring'),
        ('Agriculture & Produce', 'Agriculture & Produce'),
        ('Handicrafts & Art', 'Handicrafts & Art'),
        ('Electronics & Repair', 'Electronics & Repair'),
        ('Beauty & Wellness', 'Beauty & Wellness'),
        ('Other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    location = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='vendors/', blank=True, null=True)
    story = models.TextField()
    website = models.URLField(max_length=200, blank=True, null=True, help_text="Vendor's website or social media profile")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Contact phone number")
    email = models.EmailField(blank=True, null=True, help_text="Contact email")

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return self.name

