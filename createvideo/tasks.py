from celery import shared_task
from logic.intro.intro_methods import *
from .MainMethod import body
from django.conf import settings
from io import BytesIO
import boto3, redis , os
from datetime import datetime


### list of all slide methods ###
methods_list = [Slide1,Slide2,Slide3,Slide4]

@shared_task
def bodytest(slides_list,body_list,webhook):
    ### parse webhook data ###
    webhook_url = webhook["url"]
    meta_data = webhook["metadata"]
    user_id = meta_data["_id"]
    user_email = meta_data["employee"]
    user_name =  user_email.split('@')[0]
    video_name = user_name + user_id
    ## create new dirictory to add temperary footages of video ##
    # Get current time
    now = datetime.now()
    # Format time as HH:MM:SS
    current_time = now.strftime("%H:%M:%S")
    dir_path = os.path.join("downloads",f"{user_name}_{current_time}") 
    os.makedirs(dir_path, exist_ok=True)
    list_componant = []
    list_audios = []
    print(f"start video of: {video_name}")
    try:
        for index , slide in enumerate(slides_list):
            print(f"method index :{methods_list[index]}")
            text = slide["title"]
            audio_url = slide["audioPath"]
            duration = slide["duration"]
            start = slide["start_time"]
            image_url = slide["images"][0]["url"]
            ## download image ##
            response = requests.get(image_url)
            image_data = BytesIO(response.content)
            ### create slide content ###
            componant = methods_list[index](image_path=image_data,duration=duration,text=text,start=start,dir_path=dir_path )
            list_componant.extend(componant)
            list_audios.append((audio_url,start))
        ### intro clip of street politics ###
        intro = VideoFileClip("downloads/Street_Politics_intro.mov", has_mask=True,target_resolution=(1920,1080)).with_start(((slides_list[-1]["start_time"])+(slides_list[-1]["duration"]))-2)
        list_componant.append(intro)
        intro_audio = AudioFileClip("downloads/intro_audio.mp3").with_start((slides_list[-1]["start_time"])+(slides_list[-1]["duration"]))
        list_audios_instance = add_audios(list_audios,dir_path=dir_path)
        list_audios_instance.append(intro_audio)
        ### start body process ###
        path = body(body_list=body_list,clips=list_componant,audio_clips=list_audios_instance,video_name=video_name,webhook_url=webhook_url, meta_data=meta_data,dir_path=dir_path)
        url =  settings.MEDIA_URL + path
        payload = {
            "url": url,
            "status":"Done",
            "metadata" : meta_data
        }
        try:
            response = requests.post(webhook_url, json=payload)
            print("webhook done!")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending video notification: {e}")
            payload = {
                "status": "Failed",
                "metadata" : meta_data
            }
            requests.post(webhook_url, json=payload)
            print(f"An error occurred while sending video notification: {e}")
        
        b = is_last_task()
    except Exception as e:
        payload = {
                "status": "Failed",
                "metadata" : meta_data
            }
        requests.post(webhook_url, json=payload)
        print(f"An error occurred while rendering video due to: {e}")
        b = is_last_task()
            

    
def shutdown_instance():
    print("Shutting down the instance...")
    ec2 = boto3.client('ec2', region_name='us-east-1')
    instance_id = 'i-04c4c354b8a1c5509'  
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is stopping.")

def is_last_task(queue_name='celery', redis_host='redis', redis_port=6379, redis_db=0):
    try:
        # Connect to Redis
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

        # Get the length of the queue
        queue_length = redis_client.llen(queue_name)

        if queue_length == 0:
            print("This is the last task. No tasks are waiting in the queue.")
            shutdown_instance()
            return True

    except Exception as e:
        print(f"Error checking queue length: {e}")
        return None



@shared_task
def testsss(image_url,text,duration):
    ## download image ##
    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    # response = Slide2(image_path=image_data,text=text,start=0,duration=duration)
    # response = Slide1(image_path=image_data,text=text,start=0,duration=duration)
    # response = Slide4(image_path=image_data,text=text,start=0,duration=duration)
    response = Slide3(image_path=image_data,text=text,start=6,duration=duration)
    video = CompositeVideoClip(response,size=(1920,1080))
    output_path = f"downloads/testslide11234_testy.mp4"
    video.write_videofile(output_path, fps=30)
    