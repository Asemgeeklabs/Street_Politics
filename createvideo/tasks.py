from celery import shared_task
from logic.intro.intro_methods import *
from .MainMethod import body
from django.conf import settings

### list of all slide methods ###
methods_list = [Slide1,Slide2,Slide3,Slide4]

### method to create intro ###
@shared_task
def intro_create(slides_list):
    list_componant = []
    list_audios = []
    for index , slide in enumerate(slides_list):
        print(f"method index :{methods_list[index]}")
        text = slide["title"]
        audio_url = slide["audioPath"]
        duration = slide["duration"]
        start = slide["start_time"]
        image_url = slide["images"][0]["url"]
        ### create slide content ###
        componant = methods_list[index](image_path=image_url,duration=duration,text=text,start=start)
        list_componant.extend(componant)
        list_audios.append((audio_url,start))
    list_audios_instance = add_audios(list_audios)
    return list_audios_instance , list_componant

@shared_task
def bodytest(slides_list,body_list,webhook):
    ### parse webhook data ###
    webhook_url = webhook["url"]
    meta_data = webhook["metadata"]
    user_id = meta_data["_id"]
    user_email = meta_data["employee"]
    user_name =  user_email.split('@')[0]
    video_name = user_name + user_id
    list_componant = []
    list_audios = []
    for index , slide in enumerate(slides_list):
        print(f"method index :{methods_list[index]}")
        text = slide["title"]
        audio_url = slide["audioPath"]
        duration = slide["duration"]
        start = slide["start_time"]
        image_url = slide["images"][0]["url"]
        ### create slide content ###
        componant = methods_list[index](image_path=image_url,duration=duration,text=text,start=start)
        list_componant.extend(componant)
        list_audios.append((audio_url,start))
    list_audios_instance = add_audios(list_audios)
    ### start body process ###
    path = body(body_list=body_list,clips=list_componant,audio_clips=list_audios_instance,video_name=video_name)
    url =  settings.MEDIA_URL + path
    payload = {
        "url": url,
        "metadata" : meta_data
    }
    try:
        response = requests.post(webhook_url, json=payload)
        print("webhood done!")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending video notification: {e}")

@shared_task
def testsss(image_url,text,duration):
    response = Slide4(image_path=image_url,text=text,start=0,duration=duration)
    video = CompositeVideoClip(response)
    output_path = f"downloads/testslide4_.mp4"
    video.write_videofile(output_path, fps=30)
    