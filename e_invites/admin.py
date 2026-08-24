from django.contrib import admin
from .models import Product, Order, OrderDetails, Tag

# تسجيل جداول مشروعك الأساسي بالطريقة العادية
admin.site.register(Product)
admin.site.register(Order)

# ==========================================
# 2. تطبيق مفاهيم المحاضرة في الـ Admin
# ==========================================

# تسجيل جدول تفاصيل الطلب مع تخصيص العرض
@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'is_delivered')
    list_filter = ('is_delivered',)

# تسجيل جدول التصنيفات مع تخصيص العرض والبحث
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)