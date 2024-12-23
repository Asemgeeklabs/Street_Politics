from django.urls import path 
from .views import CreateVideo , test , Testslide4

urlpatterns = [
    path('', CreateVideo.as_view()),
    path('test/', test.as_view()),
    path('testslide4/', Testslide4.as_view()),
]