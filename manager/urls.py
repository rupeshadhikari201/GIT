from django.urls import path
from . import views
urlpatterns = [
    path('assign_project/', views.ProjectAssignView.as_view(), name='assign_project'),
    path('assigned/projects/<int:frelancer_id>/', views.GetAssignedProjectUsingFrelancerID.as_view()),
    path('project/all',views.GetAllProject.as_view(),name='get_all_project'),
    path('applied/freelancers/<int:project_id>/', views.AppliedFreelancersVeiw.as_view(), name='applied_freelancer'),
    #search users 
]
