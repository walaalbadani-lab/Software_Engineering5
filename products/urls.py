from django.urls import path
from . import views


urlpatterns = [

    # صفحة إدارة المنتجات:
    # إضافة + تعديل + عرض
    path(
        "form/",
        views.user_form_view,
        name="form"
    ),

    # تعديل
    path(
        "edit/<int:pk>/",
        views.edit_product,
        name="edit_product"
    ),

    # حذف
    path(
        "delete/<int:pk>/",
        views.delete_product,
        name="delete_product"
    ),

]
