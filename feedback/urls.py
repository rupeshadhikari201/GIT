from django.urls import path
from .views import FeedbackView

urlpatterns = [
    path('feedback/', view=FeedbackView.as_view(), name='feedback'),
]
