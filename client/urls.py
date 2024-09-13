from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ClientCreationView.as_view(), name='create_client'),
    path('detail/<int:client_id>', views.GetClientDetailsById.as_view(), name='client_details_by_id'),
    path('projects/', views.GetClientProjects.as_view(), name='get-client-project'),
    path('all/',views.GetAllClient.as_view()),
    path('projects/<int:client_id>/', views.GetClientProjectsDetailByCliendId.as_view()),

]
