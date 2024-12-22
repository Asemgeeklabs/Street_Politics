from django.urls import path 
from .views import CreateVideo , test

urlpatterns = [
    path('', CreateVideo.as_view()),
    path('test/', test.as_view()),
]