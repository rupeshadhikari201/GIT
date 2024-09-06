from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.FreelancerCreationView.as_view(), name='freelancer'),
    path('detail/', views.FreelancerDetails.as_view(), name='freelancer_details'),
    path('update/', views.UpdateFreelancerView.as_view(), name="update_frelancer"),
    path('apply/', views.ApplyProjectView.as_view(), name='apply_project'),
    path('applied/freelancers/<int:project_id>/', views.AppliedFreelancersView.as_view(), name='applied_freelancers'),
    path("all_details/", views.GetDetailsOfFrelancers.as_view()),
    path('applied_projects/',views.GetAppliedProject.as_view(), name='get_applied_project'),
    
    path('search/', views.FreelancerSearchView.as_view(), name='freelancer-search'),
]