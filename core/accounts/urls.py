from django.urls import path
from . import views
from .views import CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    # path("login", views.login_view, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("register", views.register_view, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
]
