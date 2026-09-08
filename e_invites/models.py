from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=1000)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد المراجعة'),
        ('accepted', 'تم القبول'),
        ('rejected', 'تم الرفض'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    invite_type = models.CharField(max_length=150, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True) # الحقل الجديد للتفاصيل
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # حقولك القديمة كاملة
    occasion = models.CharField(max_length=150)
    price = models.PositiveIntegerField(default=1000)
    date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    place = models.CharField(max_length=200)
    names = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.user.username if self.user else 'ضيف'} - {self.occasion}"

class OrderDetails(models.Model):
    # تم تغيير related_name من details إلى order_info لمنع التعارض
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_info")
    is_delivered = models.BooleanField(default=False)
    delivery_notes = models.TextField(blank=True)

    def __str__(self):
        return f"تفاصيل: {self.order.occasion}"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name="tags", blank=True)

    def __str__(self):
        return self.name