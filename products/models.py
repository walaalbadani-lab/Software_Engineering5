from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="الوسم"
    )

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    # علاقة من واحد إلى واحد (One-to-One)
    product = models.OneToOneField(
        'Product',
        on_delete=models.CASCADE,
        related_name="detail",
        verbose_name="المنتج"
    )
    extra_notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات إضافية"
    )

    def __str__(self):
        return f"تفاصيل: {self.product.name}"


class Product(models.Model):
    CATEGORY_CHOICES = (
        ("wedding", "دعوة زفاف"),
        ("engagement", "خطوبة"),
        ("birthday", "عيد ميلاد"),
        ("graduation", "تخرج"),
        ("other", "أخرى"),
    )

    name = models.CharField(
        max_length=200,
        verbose_name="اسم المنتج"
    )

    description = models.TextField(
        blank=True,
        default="",
        verbose_name="الوصف"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="السعر"
    )

    image = models.FileField(
        upload_to="products/",
        verbose_name="صورة أو فيديو المنتج",
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="wedding",
        verbose_name="النوع"
    )

    # علاقة من كثير إلى كثير (Many-to-Many)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="وسوم الدعوة"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.FileField(
        upload_to="products_images/",
        verbose_name="صورة أو فيديو إضافي",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"ملف إضافي لـ {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    occasion = models.CharField(
        max_length=200,
        verbose_name="مناسبة الدعوة"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="السعر"
    )

    date = models.DateField(
        verbose_name="تاريخ المناسبة"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="رقم الهاتف"
    )

    place = models.CharField(
        max_length=200,
        verbose_name="المكان"
    )

    names = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="الأسماء المطلوبة"
    )

    message = models.TextField(
        blank=True,
        verbose_name="ملاحظات أو عبارة الدعوة"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"طلب: {self.occasion} - {self.phone}"