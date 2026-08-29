from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction

from .models import Product
from .forms import ProductForm, ProductImageFormSet


@staff_member_required
def user_form_view(request, product_id=None):

    # المنتج الذي نريد تعديله
    product_obj = None

    if product_id:
        product_obj = get_object_or_404(Product, pk=product_id)

    # =========================================================
    # POST
    # =========================================================

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product_obj
        )

        formset = ProductImageFormSet(
            request.POST,
            request.FILES,
            instance=product_obj
        )

        # التحقق من الفورم والفورم الخاص بالصور قبل الدخول في transaction
        if form.is_valid() and formset.is_valid():

            try:

                # العملية كلها إما تنجح أو لا تحفظ شيئًا
                with transaction.atomic():

                    # حفظ المنتج في PostgreSQL
                    product = form.save()

                    # ربط الصور الإضافية بالمنتج
                    formset.instance = product
                    formset.save()

                # بعد انتهاء transaction بنجاح
                if product_obj:
                    messages.success(
                        request,
                        "تم تعديل الدعوة بنجاح."
                    )
                else:
                    messages.success(
                        request,
                        "تمت إضافة الدعوة بنجاح."
                    )

                # العودة لنفس صفحة الإدارة
                return redirect("form")

            except Exception as e:

                messages.error(
                    request,
                    f"حدث خطأ أثناء الحفظ: {e}"
                )

        else:

            # لا ندخل transaction إذا كانت البيانات غير صحيحة
            messages.error(
                request,
                "يرجى التأكد من صحة البيانات المدخلة."
            )

    # =========================================================
    # GET
    # =========================================================

    else:

        form = ProductForm(
            instance=product_obj
        )

        formset = ProductImageFormSet(
            instance=product_obj
        )

    # جلب المنتجات باستخدام 7 دوال QuerySet  :
    # 1. all(), 2. filter(), 3. exclude(), 4. select_related(), 5. prefetch_related(), 6. distinct(), 7. order_by()
    products = (
        Product.objects.all()
        .filter(price__gte=0)
        .exclude(category="other")
        .select_related("detail")
        .prefetch_related("images", "tags")
        .distinct()
        .order_by("-created_at")
    )

    return render(
        request,
        "products/form.html",
        {
            "form": form,
            "formset": formset,
            "products": products,
        }
    )


# =============================================================
# تعديل منتج
# =============================================================

@staff_member_required
def edit_product(request, pk):

    return user_form_view(
        request,
        product_id=pk
    )


# =============================================================
# حذف منتج
# =============================================================

@staff_member_required
def delete_product(request, pk):

    if request.method != "POST":

        messages.error(
            request,
            "طريقة الحذف غير مسموحة."
        )

        return redirect("form")

    product = get_object_or_404(
        Product,
        pk=pk
    )

    product.delete()

    messages.success(
        request,
        "تم حذف الدعوة بنجاح."
    )

    # العودة لنفس صفحة الإدارة
    return redirect("form")