from rest_framework.views import APIView
from .serializers import TemplateSerializer 
from rest_framework.response import Response
from .tasks import  intro_create , bodytest
from celery import chain
  
class test(APIView):
    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            into_data = serializer.data["slides"]
            content_data = serializer.data["body"]
            # chain(
            #     intro_create.s(slides_list=into_data),
            #     bodytest.s(body_list=content_data)
            # )()
            # audio_clips , clips = intro_create.delay(slides_list=into_data)
            bodytest.delay(slides_list=into_data,body_list=content_data)
        return Response({"message":"done!"})
    

#### endpoint for creating sp video ####
class CreateVideo(APIView):
    def post(self , request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            intro = serializer.validated_data['slides']
            content = serializer.validated_data['body']
        return Response({"message":"Done!"}) 