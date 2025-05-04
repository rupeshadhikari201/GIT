from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/user/', include('register.urls')),
   path('api/client/', include('client.urls')),
   path('api/freelancer/', include('freelancer.urls')),
   path('api/project/', include('project.urls')),
   path('api/payment/', include('payment.urls')),
   path('api/manager/', include('manager.urls')),
   path('api/newsletters/', include('newsletters.urls')),
   path('api/feedbacks/', include('feedback.urls')),
   
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
