from django.urls import path, include
from register.views import AddressDetailView, DeleteUnassignedProject, FreelancerSearchView, GetAppliedProject, GetClientDetailsById, GetClientProjects, GetProjectDetailsByIdView, LogoutView, PaymentStatusView, PriceFilterView, ProjectAssignView, ProjectFileView, ProjectStatusView, UpdateFreelancerView, UserPasswordUpdateView,UserRegistrationView, UserLoginView, UserProfileView, ChangePasswordView, SendPasswordResetEmailView, FreelancerCreationView, ClientCreationView, ProjectCreationView, SendUserVerificationLinkView, VerifyUserEmailView, ProjectUpdateView, GetUnassingedProjects, ApplyProjectView, FreelancerDetails, UpdateUserView, ProjectSearchView
# from register.views import logout_view

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns
from register import views
from register import authenticationview

# from rest_framework.routers import DefaultRouter
# from .views import ProjectStatusView
# router = DefaultRouter()
# router.register(r'project_status', ProjectStatusView)


urlpatterns = [
     path("register/", UserRegistrationView.as_view(), name="register"),
     path('login/',UserLoginView.as_view(), name='login'),
     path('profile/', UserProfileView.as_view(), name='profile'),
     path("change-password/", ChangePasswordView.as_view(), name='change_password'),
     path("password-reset-link/", SendPasswordResetEmailView.as_view(), name='password-reset-link'),
     path('user-password-update/<uid>/<token>/', UserPasswordUpdateView.as_view(), name='user-password-update'),

     path('freelancer/', FreelancerCreationView.as_view(), name='freelancer'),
     path('freelancer_details/', FreelancerDetails.as_view(), name='freelancer_details'),
     path('update/freelancer_details', UpdateFreelancerView.as_view(), name="update_frelancer"),
     path('client/', ClientCreationView.as_view(), name='client'),
     path('create_project/', ProjectCreationView.as_view(), name='create_project'),
     path('client/details/<int:client_id>', GetClientDetailsById.as_view(), name='clinet_details_by_id'),
     path('update_project/<int:project_id>', ProjectUpdateView.as_view(), name='update_project'),
     path('delete_project/<int:project_id>', DeleteUnassignedProject.as_view(), name='delete_project'),
     path('get_unassigned_project/', GetUnassingedProjects.as_view(), name='get_unassigned_project'),
     
     path('verify-user/', SendUserVerificationLinkView.as_view(), name="verify-user"),
     path('validate-email/<int>/<token>/', VerifyUserEmailView.as_view(), name="verify-email"),
     path('logout/', LogoutView.as_view(), name='logout'),
     # path('custom_logout/', logout_view, name='costom_logout'),
     
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     
     path('get-user/', views.GetUserView.as_view(), name='get_user_list'),
     path('get-user/<int:pk>/', views.GetUserView.as_view(), name='get_user_details'),
     path('update-user/', views.UpdateUserView.as_view(), name='update_user_details'),
     path('delete-user/<int:pk>/', views.GetUserView.as_view(), name='delete_user'),
     # path('get-user/', views.GetUserView, name='get_user'),
     
     path('get-client-project/', GetClientProjects.as_view(), name='get-client-project'),
     path('get-client/project/<int:project_id>/',GetProjectDetailsByIdView.as_view(),name="get_project_detail"),
     path('apply_project/', ApplyProjectView.as_view(), name='apply_project'),
     path('assign-projects/', ProjectAssignView.as_view(), name='assign-projects'),
     path('project/<int:project_id>/files/', ProjectFileView.as_view(), name='project_files'),
     path('get_applied_project/',GetAppliedProject.as_view(), name='get_applied_project'),
     
     # for authentication
     path('user-authentication/', authenticationview.UserAutheniticationExampleView.as_view(), name='user-authentication'),
     
     # include
     path('project_status/', ProjectStatusView.as_view(), name='project_status'),
     path('payment_status/', PaymentStatusView.as_view(), name='project_status'),
     # path('', include(router.urls)),
     
     # search
     path('search/', FreelancerSearchView.as_view(), name='freelancer-search'),
     path('price_filter/<int:price_start>/<int:price_end>/<int:n_applicant>', PriceFilterView.as_view(), name='price_filter'), 
     # Example usage of the ProjectSearchView API:
     # To search for projects with a title containing "web", a minimum price of 100, and a maximum of 5 applicants:
     # GET /search_project/?title=web&min_price=100&max_applicants=5
     path('search_project/', ProjectSearchView.as_view(), name='search_project'),
     
     # address url
      path('get_address/', AddressDetailView.as_view(), name='address-detail'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)