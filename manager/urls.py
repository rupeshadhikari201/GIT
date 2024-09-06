from django.urls import path
from . import views
urlpatterns = [
    path('assign_project/', views.ProjectAssignView.as_view(), name='assign_project'),
    #to get multiple project based on freelancer id
    path('assigned/projects/<int:frelancer_id>/', views.GetAssignedProjectUsingFrelancerID.as_view()),
    #to get freelancer based on project id
    path('assigned/freelancer/<int:project_id>/',views.GetAssignedFreelancerUsingProjectId.as_view()),
    path('project/all/',views.GetAllProject.as_view(),name='get_all_project'),
    path('project/assigned/',views.GetAssingedProject.as_view(),name="get_assinged_project"),
    path('applied/freelancers/<int:project_id>/', views.AppliedFreelancersVeiw.as_view(), name='applied_freelancer'),
    #search user
    path('invite/freelancer/',views.SendInvitaionToFreelancerView.as_view()),
]
