from django.urls import path 
from .views import CreateVideo , Testslide4

urlpatterns = [
    path('create_video/', CreateVideo.as_view()),
    path('testslide4/', Testslide4.as_view()),
]