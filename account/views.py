from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
import re

try:
    from account.models import UserAccount, Notification, Order
except ImportError:
    UserAccount = None
    Notification = None
    Order = None

def ok_password(p):
    return bool(re.fullmatch(r"[A-Za-z0-9\-]{6,30}", p or ""))

def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "أنت داخل مسبقاً.")
        return redirect("home")

    data = {"username": "", "email": ""}
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        p1 = request.POST.get("password1", "")
        p2 = request.POST.get("password2", "")
        data = {"username": username, "email": email}

        if len(username) < 3:
            messages.error(request, "اسم المستخدم قصير.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "هذا الاسم مسجّل مسبقاً. جرب اسماً آخر.")
        elif email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, "هذا البريد مسجّل مسبقاً.")
        elif p1 != p2:
            messages.error(request, "كلمتا السر غير متطابقتين.")
        elif not ok_password(p1):
            messages.error(request, "كلمة السر: 6 أحرف على الأقل، حروف أو أرقام أو - فقط.")
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=p1)
            except IntegrityError:
                messages.error(request, "اسم المستخدم موجود مسبقاً. جرب اسماً آخر.")
                return render(request, "account/register.html", data)

            if UserAccount is not None:
                try:
                    account, created = UserAccount.objects.get_or_create(user=user)
                    account.phone = phone 
                    account.save()
                except Exception as e:
                    print(f"Error saving to UserAccount: {e}")

            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح.")
            return redirect("home")

    return render(request, "account/register.html", data)

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "أنت داخل مسبقاً.")
        return redirect("home")
    if request.method == "POST":
        name = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        acc = User.objects.filter(username__iexact=name).first() or User.objects.filter(email__iexact=name).first()
        
        user = None
        if acc:
            user = authenticate(request, username=acc.username, password=password)
        if user:
            login(request, user)
            messages.success(request, "تم الدخول.")
            return redirect("home")
        messages.error(request, "اسم المستخدم أو كلمة السر غير صحيحة.")
    return render(request, "account/login.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "تم الخروج.")
    return redirect("home")

@login_required
@require_POST
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.link or '/')

@login_required
def order_create_view(request):
    invite_type = request.GET.get('product') or request.GET.get('type', 'دعوة عامة')
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        contact_info = request.POST.get('contact_info', '').strip()
        invite_type = request.POST.get('invite_type', invite_type)
        details = request.POST.get('details', '').strip()
        
        if not customer_name or not contact_info:
            messages.error(request, "يرجى ملء اسم العميل ومعلومات التواصل.")
        else:
            if Order is not None:
                Order.objects.create(
                    user=request.user,
                    customer_name=customer_name,
                    contact_info=contact_info,
                    invite_type=invite_type,
                    details=details
                )
            
            if Notification is not None:
                Notification.objects.create(
                    recipient=request.user,
                    message=f"تم الطلب لـ ({invite_type}) بنجاح وبانتظار الرد.",
                    link="/"
                )
                
                admins = User.objects.filter(is_staff=True)
                for admin in admins:
                    Notification.objects.create(
                        recipient=admin,
                        message=f"طلب تصميم جديد ({invite_type}) من العميل: {customer_name}.",
                        link="/"
                    )
                
            messages.success(request, "تم الطلب وبانتظار الرد.")
            return redirect("home")
            
    return render(request, "account/order_form.html", {"invite_type": invite_type})

# --- دالة قبول الطلب من قبل الأدمن وتحديث حالته وإرسال إشعار للمستخدم ---
@login_required
@require_POST
def accept_order_view(request, pk):
    if not request.user.is_staff:
        messages.error(request, "غير مصرح لك بهذا الإجراء.")
        return redirect("home")
    
    order = get_object_or_404(Order, pk=pk)
    
    # تحديث حالة الطلب إذا كان الحقل موجوداً لضمان حفظ القبول
    if hasattr(order, 'status'):
        order.status = 'accepted'
        order.save()
    if hasattr(order, 'is_completed'):
        order.is_completed = True
        order.save()

    # إرسال إشعار للمستخدم بأن طلبه قُبل ليظهر له عند الضغط على الجرس
    if Notification is not None and order.user:
        Notification.objects.create(
            recipient=order.user,
            message=f"تهانينا! تم قبول طلبك الخاص بـ ({order.invite_type}) بنجاح 🎉",
            link="/"
        )
    messages.success(request, f"تم قبول طلب العميل {order.customer_name} بنجاح.")
    return redirect("home")

# --- دالة رفض الطلب من قبل الأدمن وتحديث حالته وإرسال إشعار للمستخدم ---
@login_required
@require_POST
def reject_order_view(request, pk):
    if not request.user.is_staff:
        messages.error(request, "غير مصرح لك بهذا الإجراء.")
        return redirect("home")
    
    order = get_object_or_404(Order, pk=pk)
    
    # تحديث حالة الطلب إلى مرفوض
    if hasattr(order, 'status'):
        order.status = 'rejected'
        order.save()

    # إرسال إشعار للمستخدم بأن طلبه رُفض
    if Notification is not None and order.user:
        Notification.objects.create(
            recipient=order.user,
            message=f"نأسف، تم رفض طلبك الخاص بـ ({order.invite_type}).",
            link="/"
        )
    messages.success(request, f"تم رفض طلب العميل {order.customer_name}.")
    return redirect("home")