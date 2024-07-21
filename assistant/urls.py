from django.urls import path
from .views import AssistantView

urlpatterns = [
    path('upload/', AssistantView.as_view(), name='file-upload'),
]
