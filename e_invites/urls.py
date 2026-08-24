from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("order/", views.order, name="order"),
    path("products/", views.product_list, name="product_list"),
    path("assignment/", views.assignment_queries, name="assignment_queries"),
    path("edit/<int:order_id>/", views.edit_order, name="edit_order"),
    path("form/", views.user_form_view, name="form"),
    path("form/<int:product_id>/", views.user_form_view, name="edit_product_form"),
    path("form/delete/<int:product_id>/", views.delete_product, name="delete_product"),
]