from rest_framework.views import APIView
from .serializers import TemplateSerializer , SlidesSerializer
from rest_framework.response import Response
from .tasks import   bodytest , testsss
from logic.intro.intro_methods import *
  
class CreateVideo(APIView):
    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            webhook = serializer.data["webhock"]
            response = serializer.data["response"]
            into_data = response["slides"]
            content_data = response["body"]
            bodytest.delay(slides_list=into_data,body_list=content_data,webhook=webhook)
        return Response({"message":"done!"})
    
class Testslide4(APIView):
    def post(self , request):
        serializer = SlidesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            text = serializer.data["title"]
            duration = serializer.data["duration"]
            image_url = serializer.data["images"][0]["url"]
            testsss.delay(image_url,text,duration)
        return Response({"message":"Done!"}) 
