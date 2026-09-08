from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("order/", views.order, name="order"),
    path("about/", views.about, name="about"),
    path("products/", views.product_list, name="product_list"),
    path("create-order/", views.create_order, name="create_order"),
    path("order/accept/<int:pk>/", views.accept_order, name="accept_order"),
    path("order/reject/<int:pk>/", views.reject_order, name="reject_order"),
    path("notification/read/<int:pk>/", views.mark_as_read, name="mark_as_read"),
]