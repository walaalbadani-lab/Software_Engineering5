from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

# أضفنا استيراد جدول Product من تطبيق products لكي تظهر المنتجات المضافة من الأدمن
from .models import Order
from products.models import Product
from .forms import OrderForm, ProductForm

PRICES = {
    "رسم رقمي": 1000,
    "مواليد": 1000,
    "زفاف": 1000,
    "تخرج": 1000,
    "فيديو": 300,
    "جرائد وورقيات": 500,
}

def home(request):
    notes = list(Order.objects.all()[:8])
    return render(
        request,
        "e_invites/home.html",
        {
            "products": Product.objects.all(),
            "q": (request.GET.get("q") or "").strip(),
            "notifications": notes,
            "notification_count": Order.objects.count(),
        },
    )

def about(request):
    return render(request, "e_invites/about.html")

def product_list(request):
    return redirect("home")

def order(request):
    selected = (
        request.POST.get("occasion") or request.GET.get("product") or ""
    ).strip()

    if request.method == "POST":
        price = PRICES.get(selected)
        if price is None:
            product = Product.objects.filter(title=selected).first()
            if product is None:
                product = Product.objects.filter(name=selected).first()
            price = int(getattr(product, "price", 0) or 0) if product else None

        event_date = parse_date(request.POST.get("date") or "")
        phone = request.POST.get("phone", "").strip()
        place = request.POST.get("place", "").strip()

        if not selected or price is None:
            messages.error(request, "اختر نوع الدعوة.")
        elif not event_date:
            messages.error(request, "أدخل التاريخ.")
        elif not phone or not place:
            messages.error(request, "أكمل المكان ورقم التواصل.")
        else:
            Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                occasion=selected,
                price=price,
                date=event_date,
                phone=phone,
                place=place,
                names=request.POST.get("names", "").strip(),
                message=request.POST.get("message", "").strip(),
            )
            messages.success(request, "تم تسجيل الطلب.")
            return redirect("home")

    return render(
        request,
        "e_invites/order.html",
        {
            "selected_product": selected,
        },
    )

def assignment_queries(request):
    all_orders = Order.objects.all()

    try:
        single_product = Product.objects.get(id=1)
    except Product.DoesNotExist:
        single_product = None

    filtered_orders = Order.objects.filter(price=1000)
    excluded_orders = Order.objects.exclude(occasion="زفاف")
    orders_count = Order.objects.count()
    ordered_orders = Order.objects.order_by("-created_at")
    first_order = Order.objects.first()

    context = {
        "all_orders": all_orders,
        "single_product": single_product,
        "filtered_orders": filtered_orders,
        "excluded_orders": excluded_orders,
        "count": orders_count,
        "ordered_orders": ordered_orders,
        "first_order": first_order,
    }

    return render(request, "e_invites/home.html", context)

def edit_order(request, order_id):
    try:
        order_obj = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "الطلب غير موجود.")
        return redirect("home")

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الطلب بنجاح!")
            return redirect("home")
    else:
        form = OrderForm(instance=order_obj)

    return render(
        request,
        "e_invites/edit_order.html",
        {"form": form, "order": order_obj},
    )

def user_form_view(request, product_id=None):
    if product_id:
        product_obj = get_object_or_404(Product, id=product_id)
    else:
        product_obj = None

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم حفظ البيانات بنجاح!")
            return redirect("form")
    else:
        form = ProductForm(instance=product_obj)

    products = Product.objects.all()

    return render(
        request,
        "e_invites/form.html",
        {
            "form": form,
            "products": products,
        },
    )

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "تم حذف المنتج بنجاح!")
    return redirect("form")