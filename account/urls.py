from django.urls import path
from account.views import UserPasswordUpdateView, UserRegistrationView, UserLoginView, UserProfileView, ChangePasswordView, SendPasswordResetEmailView

urlpatterns = [
     path("register/", UserRegistrationView.as_view(), name="register"),
     path('login/',UserLoginView.as_view(), name='login'),
     path('profile/', UserProfileView.as_view(), name='profile'),
     path("change-password/", ChangePasswordView.as_view(), name='change_password'),
     path("password-reset-link/", SendPasswordResetEmailView.as_view(), name='password-reset-link'),
     path('user-password-update/<uid>/<token>/', UserPasswordUpdateView.as_view(), name='user-password-update')
]
