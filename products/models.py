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
    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # الحقول المطلوبة لواجهة الطلبات الجديدة
    customer_name = models.CharField(
        max_length=200,
        verbose_name="اسم العميل",
        blank=True,
        null=True
    )

    contact_info = models.CharField(
        max_length=50,
        verbose_name="رقم الهاتف / واتساب",
        blank=True,
        null=True
    )

    invite_type = models.CharField(
        max_length=100,
        verbose_name="نوع الدعوة",
        blank=True,
        null=True
    )

    details = models.TextField(
        blank=True,
        verbose_name="تفاصيل إضافية"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="حالة الطلب"
    )

    # الحقول القديمة احتفظنا بها اختيارية (blank=True, null=True) لمنع أي تعارض
    occasion = models.CharField(
        max_length=200,
        verbose_name="مناسبة الدعوة",
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="السعر",
        blank=True,
        null=True
    )

    date = models.DateField(
        verbose_name="تاريخ المناسبة",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="رقم الهاتف",
        blank=True,
        null=True
    )

    place = models.CharField(
        max_length=200,
        verbose_name="المكان",
        blank=True,
        null=True
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
        return f"طلب: {self.customer_name or self.occasion} - {self.contact_info or self.phone}"