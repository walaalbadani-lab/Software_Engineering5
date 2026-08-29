from django.shortcuts import render
from products.models import Product, Order
from products.forms import ProductForm


def home(request):

    q = request.GET.get("q", "").strip()

    if q:
        products = Product.objects.filter(
            name__icontains=q
        ).order_by("-created_at")
    else:
        products = Product.objects.all().order_by("-created_at")

    notifications = []

    if request.user.is_authenticated:
        notifications = Order.objects.filter(
            user=request.user
        ).order_by("-created_at")[:5]

    # نموذج إضافة منتج
    form = ProductForm()

    context = {
        "products": products,
        "q": q,
        "notifications": notifications,
        "notification_count": len(notifications),
        "form": form,
    }

    return render(
        request,
        "e_invites/home.html",
        context
    )


def order(request):

    products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "products/list.html",
        {
            "products": products
        }
    )


def about(request):

    products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "products/list.html",
        {
            "products": products
        }
    )


def product_list(request):

    products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "products/list.html",
        {
            "products": products
        }
    )