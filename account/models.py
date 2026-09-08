from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الجوال")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True, default='/')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient.username} - {self.message}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_orders', blank=True, null=True)
    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    contact_info = models.CharField(max_length=100, verbose_name="رقم الهاتف / واتساب")
    invite_type = models.CharField(max_length=50, verbose_name="نوع الدعوة")
    details = models.TextField(verbose_name="التفاصيل")
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False, verbose_name="تم الانجاز")
    
    # الحقل الجديد المضاف لتتبع حالة الطلب دون حذف أي كود قديم
    status = models.CharField(max_length=20, default='pending', verbose_name="حالة الطلب")

    def __str__(self):
        return f"طلب: {self.customer_name} ({self.invite_type})"