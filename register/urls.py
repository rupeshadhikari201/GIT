from django.urls import path, include
from register.views import AddressDetailView,LogoutView, UserPasswordUpdateView, UserProfileByIdView,UserRegistrationView, UserLoginView, UserProfileView, ChangePasswordView,SendUserVerificationLinkView, VerifyUserEmailView, SendPasswordResetEmailView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns
from register import views
from register import authenticationview

# from rest_framework.routers import DefaultRouter
# from .views import ProjectStatusView
# router = DefaultRouter()
# router.register(r'project_status', ProjectStatusView)


urlpatterns = [
     path("user/", UserRegistrationView.as_view(), name="user_registration"),
     path('login/',UserLoginView.as_view(), name='user_login'),
     path('profile/', UserProfileView.as_view(), name='profile'),
     path('profile/<int:user_id>/', UserProfileByIdView.as_view(), name='profile_by_id'),
     path("change_password/", ChangePasswordView.as_view(), name='change_password'),
     path("reset_password/", SendPasswordResetEmailView.as_view(), name='reset_password'),
     path('update_password/<uid>/<token>/', UserPasswordUpdateView.as_view(), name='update_password'),
     path('send_verification/', SendUserVerificationLinkView.as_view(), name='send_verification'),
     path('verify_email/<uid>/<token>/', VerifyUserEmailView.as_view(), name="verify_email"),
     path('get_all_users/', views.GetUserView.as_view(), name='get_all_users'),
     path('get_user_details/<int:pk>/', views.GetUserView.as_view(), name='get_user_details'),
     path('update_user_details/', views.UpdateUserView.as_view(), name='update_user_details'),
     path('get_address/', AddressDetailView.as_view(), name='address-detail'),
     
     path('logout/', LogoutView.as_view(), name='logout'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     
     # for authentication
     path('user-authentication/', authenticationview.UserAutheniticationExampleView.as_view(), name='user-authentication'),
    
] 

urlpatterns = format_suffix_patterns(urlpatterns)