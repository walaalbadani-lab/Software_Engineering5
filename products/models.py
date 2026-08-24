from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('wedding', 'دعوة زفاف'),
        ('engagement', 'خطوبة'),
        ('birthday', 'عيد ميلاد'),
        ('graduation', 'تخرج'),
        ('other', 'أخرى'),
    )
    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    description = models.TextField(blank=True, default='', verbose_name="الوصف")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="السعر")
    
    # تم تغييرها إلى FileField لتقبل ملفات الفيديو والصور معاً
    image = models.FileField(upload_to='products/', verbose_name="صورة أو فيديو المنتج", blank=True, null=True)
    
    # أو يمكنك إضافة حقل منفصل للفيديو هكذا:
    # video = models.FileField(upload_to='products/videos/', verbose_name="ملف الفيديو", blank=True, null=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='wedding', verbose_name="النوع")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name