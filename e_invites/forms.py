from django import forms
from .models import OrderDetails, Tag, Order, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'image']
        labels = {
            'title': 'اسم الدعوة / المنتج',
            'price': 'السعر',
            'image': 'صورة المنتج',
        }
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}),
            'price': forms.NumberInput(attrs={'style': 'width: 100%; padding: 8px;'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['occasion', 'phone', 'place', 'names', 'message']
        labels = {
            'occasion': 'المناسبة',
            'phone': 'رقم التواصل',
            'place': 'المكان',
            'names': 'الأسماء',
            'message': 'الرسالة',
        }

class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = ['order', 'is_delivered', 'delivery_notes']
        widgets = {
            'delivery_notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'order': 'الطلب المرتبط',
            'is_delivered': 'تم التوصيل',
            'delivery_notes': 'ملاحظات التوصيل',
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'products']
        labels = {
            'name': 'اسم التصنيف',
            'products': 'الطلبات المرتبطة',
        }