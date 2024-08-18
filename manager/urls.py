from django.urls import path
from . import views
urlpatterns = [
    path('assign_project/', views.ProjectAssignView.as_view(), name='assign_project'),
    path('assigned_projects/<int:frelancer_id>/', views.GetAssignedProjectUsingFrelancerID.as_view()),
]
