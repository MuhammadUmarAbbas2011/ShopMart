from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
class Stores(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Tech'),
        ('CLOTHING', 'Clothing'),
        ('FOOD', 'Food'),
        ('FURNITURE', 'Furniture'),
        ('BEAUTY', 'Beauty'),
        ('SPORTS', 'Sports'),
        ('AUTOMOTIVE', 'Automotive'),
        ('TOYS', 'Toys'),
        ('BOOKS', 'Books'),
        ('MUSIC', 'Music'),
        ('HEALTH', 'Health'),
        ('HOME_APPLIANCES', 'Home Appliances'),
        ('GROCERY', 'Grocery'),
        ('JEWELRY', 'Jewelry'),
        ('PET_SUPPLIES', 'Pet Supplies'),
        ('ELECTRONICS', 'Electronics'),
        ('BABY_PRODUCTS', 'Baby Products'),
        ('GARDENING', 'Gardening'),
        ('OFFICE_SUPPLIES', 'Office Supplies'),
        ('TRAVEL', 'Travel'),
        ('OUTDOOR', 'Outdoor & Camping'),
        ('VIDEO_GAMES', 'Video Games'),
        ('HANDMADE', 'Handmade & Crafts'),
        ('LUXURY', 'Luxury Items'),
        ('MEDICAL', 'Medical & Pharmacy'),
        ('INDUSTRIAL', 'Industrial & Tools'),
        ('GIFTS', 'Gifts & Collectibles'),
        ('MOVIES', 'Movies & Entertainment'),
        ('HOME_DECOR', 'Home Decor'),
        ('ART', 'Art & Paintings'),
        ('HOBBIES', 'Hobbies & DIY'),
        ('SECURITY', 'Security & Surveillance'),
        ('BICYCLES', 'Bicycles & Accessories'),
        ('WATCHES', 'Watches'),
        ('FARMING', 'Farming & Agriculture'),
        ('REAL_ESTATE', 'Real Estate'),
        ('EDUCATION', 'Education & e-Learning'),
        ('GAMING', 'Gaming'),
        ('FASHION', 'Fashion'),
        ('SPIRITUAL', 'Spiritual & Religious'),
        ('MOTORS', 'Motorcycles & Scooters'),
        ('RESTAURANTS', 'Restaurants & Cafes'),
        ('BAKERY', 'Bakery & Confectionery'),
        ('WEDDINGS', 'Weddings & Events'),
        ('PHOTOGRAPHY', 'Photography & Videography'),
        ('MUSICAL_INSTRUMENTS', 'Musical Instruments'),
        ('TEA_COFFEE', 'Tea & Coffee'),
        ('FISHING', 'Fishing & Hunting'),
        ('DRONES', 'Drones & RC Gadgets'),
        ('ENERGY', 'Solar & Renewable Energy'),
        ('VR_AR', 'VR & AR Equipment'),
        ('FITNESS', 'Fitness & Gym Equipment'),
    ]

    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='Store_Images/')
    unique_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.by_user.username} - {self.get_category_display()}"


class Products(models.Model):
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=50, choices=Stores.CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class CartModel(models.Model):
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    by_product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('by_user', 'by_product')

    def __str__(self):
        return f"{self.by_user.username} - {self.by_product.name} x {self.quantity}"


class CheckoutModel(models.Model):
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Products)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)
    shipping_address = models.TextField()
    payment_status = models.CharField(max_length=20, default="Pending")
    slug = models.SlugField(unique=True, blank=True)  
    tracking_id = models.CharField(max_length=15, unique=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(str(uuid.uuid4())[:8]) 
        if not self.tracking_id:  
            self.tracking_id = str(uuid.uuid4())[:15]
        super().save(*args, **kwargs)

class OrderModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('in_warehouse', 'IN OUR WAREHOUSE'),
        ('in_your_city', 'IN YOUR CITY'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Products')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)
    shipping_address = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    tracking_id = models.CharField(max_length=15, unique=True, blank=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def can_delete(self):
        return self.order_status == 'pending'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.by_user.username}-{uuid.uuid4().hex[:6]}")
        if not self.tracking_id:
            self.tracking_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order by {self.by_user.username} - {self.tracking_id}"
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE) 
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"