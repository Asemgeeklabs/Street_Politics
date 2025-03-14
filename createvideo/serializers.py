from rest_framework import serializers

### serializer for images or videos ###
class ImagesSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()
    duration = serializers.FloatField(required=False)
    

### serializer for slides ###
class SlidesSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    audioPath = serializers.URLField()
    duration = serializers.FloatField()
    start_time = serializers.FloatField()
    images = ImagesSerializer(many=True)

### serializer for body ###
class BodySerializer(serializers.Serializer):
    audioPath = serializers.URLField(required=False)
    url = serializers.URLField(required=False)
    duration = serializers.FloatField(required=False)
    start_time = serializers.FloatField()
    images = ImagesSerializer(many=True,required=False)

### serializer for template ###
class ResponseSerializer(serializers.Serializer):
    slides = SlidesSerializer(many=True)
    body = BodySerializer(many=True)

class MetadataSerializer(serializers.Serializer):
    _id = serializers.CharField()
    employee = serializers.EmailField()

# Webhook Serializer
class WebhockSerializer(serializers.Serializer):
    url = serializers.URLField()
    metadata = MetadataSerializer()

### main template ###
class TemplateSerializer(serializers.Serializer):
    webhock = WebhockSerializer() 
    response = ResponseSerializer()