from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.ProjectCreationView.as_view(), name='create_project'),
    path('update/<int:project_id>', views.ProjectUpdateView.as_view(), name='update_project'),
    path('delete/<int:project_id>', views.DeleteUnassignedProject.as_view(), name='delete_project'),
    path('unassigned/', views.GetUnassingedProjects.as_view(), name='get_unassigned_project'),
    path('price_filter/<int:price_start>/<int:price_end>/<int:n_applicant>',views.PriceFilterView.as_view(), name='price_filter'), 
    path('search/', views.ProjectSearchView.as_view(), name='search_project'),
    path('detail/<int:project_id>/',views.GetProjectDetailsByIdView.as_view(),name="get_project_detail"),
    path('files/<int:project_id>/', views.ProjectFileView.as_view(), name='project_files'),
    path('status/', views.ProjectStatusView.as_view(), name='project_status'),
]
