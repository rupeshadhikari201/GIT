from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls 
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/register/', include('register.urls')),
   path('api/client/', include('client.urls')),
   path('api/freelacer/', include('freelancer.urls')),
   path('api/project/', include('project.urls')),
   path('api/payment/', include('payment.urls')),
   path('api/manager/', include('manager.urls')),
   
   path('docs/', include_docs_urls(title="API")),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# customize the Django Admin 
admin.site.site_title  = "GokapInnoTech"
admin.site.site_header = "Gokap Administration"
admin.site.index_title = "Gokap"

# Configure urls.py to serve media files during development and production both. 
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
   urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

'''The static function from django.conf.urls.static is used to add URL patterns that serve files from the MEDIA_ROOT directory at the URL specified by MEDIA_URL'''
