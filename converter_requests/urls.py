from django.urls import path
from .views import TextSendView

urlpatterns = [
    path('', TextSendView.as_view()),
    
]