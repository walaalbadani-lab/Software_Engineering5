from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "category",
            "image",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "اسم المنتج",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "الوصف",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "السعر",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            filename = image.name.lower()
            # تحديد الامتدادات المسموح بها بدقة لمنع رفع الملفات الصوتية أو الخاطئة
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.mov', '.avi', '.webm']
            if not any(filename.endswith(ext) for ext in valid_extensions):
                raise ValidationError("يرجى رفع ملف صالح (صورة مثل jpg, png أو فيديو مثل mp4).")
        return image


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=["image"],
    extra=1,
    can_delete=True
)