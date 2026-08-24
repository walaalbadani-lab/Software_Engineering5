from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
import re

try:
    from account.models import UserAccount
except ImportError:
    UserAccount = None

def ok_password(p):
    return bool(re.fullmatch(r"[A-Za-z0-9\-]{6,30}", p or ""))

def register_view(request):
    # تم إيقاف هذا الشرط عشان تقدري تسجلي مستخدمين وإنتي داخلة بحساب الإدمن
    # if request.user.is_authenticated:
    #     messages.info(request, "أنت داخل مسبقاً.")
    #     return redirect("home")

    data = {"username": "", "email": ""}
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        
        # استلام رقم الجوال من واجهة التسجيل
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
                # 1. حفظ المستخدم في جدول المصادقة الأساسي
                user = User.objects.create_user(username=username, email=email, password=p1)
            except IntegrityError:
                messages.error(request, "اسم المستخدم موجود مسبقاً. جرب اسماً آخر.")
                return render(request, "account/register.html", data)

            # 2. حفظ المستخدم في جدولك الخاص (UserAccount)
            if UserAccount is not None:
                try:
                    account, created = UserAccount.objects.get_or_create(user=user)
                    account.phone = phone 
                    account.save()
                except Exception as e:
                    print(f"Error saving to UserAccount: {e}")

            messages.success(request, "تم إنشاء الحساب بنجاح.")
            return redirect("home")

    return render(request, "account/register.html", data)


# --- دالة تسجيل الدخول ---
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


# --- دالة تسجيل الخروج ---
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "تم الخروج.")
    return redirect("home")