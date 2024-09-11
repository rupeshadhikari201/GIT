from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.FreelancerCreationView.as_view(), name='freelancer'),
    path('detail/', views.FreelancerDetails.as_view(), name='freelancer_details'),
    path('update/', views.UpdateFreelancerView.as_view(), name="update_frelancer"),
    path('apply/', views.ApplyProjectView.as_view(), name='apply_project'),
    path("all/details/", views.GetDetailsOfFrelancers.as_view()),
    path('applied/projects/',views.GetAppliedProject.as_view(), name='get_applied_project'),
    path('applied/projects/<int:applied_id>/',views.GetAppliedProjectById.as_view(), name='get_applied_project'),
    path('search/', views.FreelancerSearchView.as_view(), name='freelancer-search'),
]
