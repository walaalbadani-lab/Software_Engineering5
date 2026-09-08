from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("notifications/<int:pk>/read/", views.mark_as_read, name="mark_as_read"),
    path("order/new/", views.order_create_view, name="create_order"),
    path("order/<int:pk>/accept/", views.accept_order_view, name="accept_order"),
    path("order/<int:pk>/reject/", views.reject_order_view, name="reject_order"),
]