from django.urls import path
from register.views import GetCreatedProjects, ProjectAssignView, UserPasswordUpdateView,UserRegistrationView, UserLoginView, UserProfileView, ChangePasswordView, SendPasswordResetEmailView, FreelancerCreationView, ClientCreationView, ProjectCreationView, SendUserVerificationLinkView, VerifyUserEmailView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns
from register import views


urlpatterns = [
     path("register/", UserRegistrationView.as_view(), name="register"),
     path('login/',UserLoginView.as_view(), name='login'),
     path('profile/', UserProfileView.as_view(), name='profile'),
     path("change-password/", ChangePasswordView.as_view(), name='change_password'),
     path("password-reset-link/", SendPasswordResetEmailView.as_view(), name='password-reset-link'),
     path('user-password-update/<uid>/<token>/', UserPasswordUpdateView.as_view(), name='user-password-update'),

     path('freelancer/', FreelancerCreationView.as_view(), name='freelancer'),
     path('client/', ClientCreationView.as_view(), name='client'),
     path('create_project/', ProjectCreationView.as_view(), name='create_project'),
     
     path('verify-user/', SendUserVerificationLinkView.as_view(), name="verify-user"),
     path('validate-email/<int>/<token>/', VerifyUserEmailView.as_view(), name="verify-email"),
     
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     
     path('get-user/', views.GetUserView.as_view(), name='get_user_list'),
     path('get-user/<int:pk>/', views.GetUserView.as_view(), name='get_user_details'),
     path('update-user/', views.UpdateUserView.as_view(), name='update_user_details'),
     path('delete-user/<int:pk>/', views.GetUserView.as_view(), name='delete_user'),
     # path('get-user/', views.GetUserView, name='get_user'),
     
     path('get-client-project/', GetCreatedProjects.as_view(), name='get-client-project'),
     
     path('assign-projects/', ProjectAssignView.as_view(), name='assign-projects')
] 

urlpatterns = format_suffix_patterns(urlpatterns)