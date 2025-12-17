from django.urls import path
from users.api.user_profile import views

urlpatterns = [
    path("register_user/", views.SignupView.as_view(), name="register user"),
    path("login_user/", views.LoginView.as_view(), name="login user"),
    path("logout_user/", views.LogoutView.as_view(), name="logout user"),
]