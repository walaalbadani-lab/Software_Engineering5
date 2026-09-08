from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
    orders = []

    if request.user.is_authenticated:
        # جلب طلبات المستخدم الخاصّة لعرض حالة (قبول/رفض)
        notifications = Order.objects.filter(
            user=request.user
        ).order_by("-created_at")
        
        # إذا كان المستخدم أدمن، يتم جلب جميع الطلبات للتحكم بها
        if request.user.is_staff:
            orders = Order.objects.all().order_by("-created_at")

    form = ProductForm()

    context = {
        "products": products,
        "q": q,
        "notifications": notifications,
        "notification_count": notifications.filter(status='pending').count() if request.user.is_authenticated else 0,
        "orders": orders,
        "form": form,
    }

    return render(
        request,
        "e_invites/home.html",
        context
    )


def create_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        contact_info = request.POST.get('contact_info')
        invite_type = request.POST.get('invite_type')
        details = request.POST.get('details')
        
        Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=customer_name,
            contact_info=contact_info,
            invite_type=invite_type,
            details=details,
            status='pending'
        )
        messages.success(request, "تم إرسال طلبك بنجاح! سيتم مراجعته قريباً.")
    return redirect('home')


def order(request):
    if request.method == 'POST':
        return create_order(request)
    products = Product.objects.all().order_by("-created_at")
    return render(request, "products/list.html", {"products": products})


def about(request):
    products = Product.objects.all().order_by("-created_at")
    return render(request, "products/list.html", {"products": products})


def product_list(request):
    products = Product.objects.all().order_by("-created_at")
    return render(request, "products/list.html", {"products": products})


# قبول الطلب من قبل الأدمن
def accept_order(request, pk):
    if request.user.is_staff:
        order_item = get_object_or_404(Order, pk=pk)
        order_item.status = 'accepted'
        order_item.save()
        messages.success(request, f"تم قبول طلب العميل {order_item.customer_name} بنجاح.")
    return redirect('home')


# رفض الطلب من قبل الأدمن
def reject_order(request, pk):
    if request.user.is_staff:
        order_item = get_object_or_404(Order, pk=pk)
        order_item.status = 'rejected'
        order_item.save()
        messages.success(request, f"تم رفض طلب العميل {order_item.customer_name}.")
    return redirect('home')


def mark_as_read(request, pk):
    return redirect('home')