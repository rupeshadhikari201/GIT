from django.urls import path, include
from register.views import AddressDetailView, \
            LogoutView, UserPasswordUpdateView, \
            UserProfileByIdView,UserRegistrationView,\
            UserLoginView, UserProfileView, ChangePasswordView,\
            SendUserVerificationLinkView, VerifyUserEmailView,\
            SendPasswordResetEmailView,UserGoogleLoginView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns
from register import views

urlpatterns = [
     path("register/", UserRegistrationView.as_view(), name="user"),
     path('login/',UserLoginView.as_view(), name='login'),
     path('login/google/',UserGoogleLoginView.as_view(), name='google_login'),
     path('profile/', UserProfileView.as_view(), name='profile'),
     path('profile/<int:user_id>/', UserProfileByIdView.as_view(), name='profile_by_id'),
     path("change_password/", ChangePasswordView.as_view(), name='change_password'),
     path("reset_password/", SendPasswordResetEmailView.as_view(), name='reset_password'),
     path('update_password/<uid>/<token>/', UserPasswordUpdateView.as_view(), name='update_password'),
     path('send/verification/', SendUserVerificationLinkView.as_view(), name='send_verification'),
     path('verify_email/<int>/<token>/', VerifyUserEmailView.as_view(), name="verify-email"),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('all/users/', views.GetUserView.as_view(), name='get_user_list'),
     path('<int:pk>/', views.GetUserView.as_view(), name='get_user_details'),
     path('update/', views.UpdateUserView.as_view(), name='update_user_details'),
     path('delete/<int:pk>/', views.GetUserView.as_view(), name='delete_user'),
  
      path('address/', AddressDetailView.as_view(), name='address-detail'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)