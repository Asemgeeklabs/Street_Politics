from rest_framework.views import APIView
from .serializers import TemplateSerializer , SlidesSerializer
from rest_framework.response import Response
from .tasks import   bodytest , testsss
from logic.intro.intro_methods import *
  
class test(APIView):
    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            webhook = serializer.data["webhock"]
            response = serializer.data["response"]
            into_data = response["slides"]
            content_data = response["body"]
            bodytest.delay(slides_list=into_data,body_list=content_data,webhook=webhook)
        return Response({"message":"done!"})
    

#### endpoint for creating sp video ####
class CreateVideo(APIView):
    def post(self , request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            intro = serializer.validated_data['slides']
            content = serializer.validated_data['body']
        return Response({"message":"Done!"}) 

"""
{
                "title": "Peterson's Momentous Claim",
                "audioPath": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-S1-1734857457171.mp3",
                "duration": 19.644063,
                "start_time": 30.171312,
                "images": [
                    {
                        "url": "https://dl.claid.ai/7c357007-19a7-45d3-98a0-d4ad160a71e1/800px-Jordan_Peterson_by_Gage_Skidmore.jpeg",
                        "pause_duration": 30.171312
                    }
                ]
            }
"""

class Testslide4(APIView):
    def post(self , request):
        serializer = SlidesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            text = serializer.data["title"]
            duration = serializer.data["duration"]
            image_url = serializer.data["images"][0]["url"]
            testsss.delay(image_url,text,duration)
        return Response({"message":"Done!"}) 
