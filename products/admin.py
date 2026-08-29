from django.contrib import admin

from .models import Product, ProductImage, ProductDetail, Tag


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# إضافة Inline لعلاقة الواحد إلى الواحد (One-to-One) وتطبيق مفاهيم المحاضرة
class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    can_delete = False
    verbose_name_plural = "التفاصيل الإضافية"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "category",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "category",
    )

    # تم دمج علاقة One-to-One و الـ Inlines مع الحفاظ على كودك الأصلي بالكامل
    inlines = [
        ProductImageInline,
        ProductDetailInline,
    ]

    # إضافة حقل علاقة Many-to-Many (الوسوم) بشكل احترافي داخل لوحة التحكم
    filter_horizontal = ('tags',)


# تسجيل نموذج الوسوم (Many-to-Many) ليظهر في لوحة التحكم
admin.site.register(Tag)