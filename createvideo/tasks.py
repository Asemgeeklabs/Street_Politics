from celery import shared_task
from logic.intro.intro_methods import *
from .MainMethod import body
from django.conf import settings
from io import BytesIO
import boto3, redis
import os
import traceback
import shutil
import tempfile
import contextlib

### list of all slide methods ###
methods_list = [Slide1, Slide2, Slide3, Slide4]

@shared_task
def bodytest(slides_list, body_list, webhook):
    ### parse webhook data ###
    webhook_url = webhook["url"]
    meta_data = webhook["metadata"]
    user_id = meta_data["_id"]
    user_email = meta_data["employee"]
    user_name = user_email.split('@')[0]
    video_name = user_name + user_id
    list_componant = []
    list_audios = []
    all_clips = []  # Track all clips for proper cleanup
    
    print(f"start video of: {video_name}")
    try:
        for index, slide in enumerate(slides_list):
            print(f"method index :{methods_list[index]}")
            text = slide["title"]
            audio_url = slide["audioPath"]
            duration = slide["duration"]
            start = slide["start_time"]
            image_url = slide["images"][0]["url"]
            
            try:
                ## download image with better error handling ##
                response = requests.get(image_url)
                response.raise_for_status()  # Check for HTTP errors
                
                # Create a copy of the image data to ensure it stays open
                image_data = BytesIO(response.content)
                image_data_copy = BytesIO(image_data.getvalue())
                
                ### create slide content ###
                componant = methods_list[index](
                    image_path=image_data_copy,
                    duration=duration,
                    text=text,
                    start=start
                )
                list_componant.extend(componant)
                list_audios.append((audio_url, start))
                
                # Clean up
                image_data.close()
            except Exception as e:
                print(f"Error processing slide {index}: {str(e)}")
                traceback.print_exc()
        
        # Handle intro audio with better resource management
        try:
            audio_file_path = "downloads/intro_audio.mp3"
            print(f"Loading intro_audio from {os.path.abspath(audio_file_path)}")
            
            # Check if file exists first
            if not os.path.exists(audio_file_path):
                print(f"WARNING: Audio file {audio_file_path} does not exist!")
            else:
                # Create a temporary directory and copy the audio file
                temp_dir = tempfile.mkdtemp()
                temp_audio_path = os.path.join(temp_dir, "intro_audio_temp.mp3")
                
                try:
                    # Copy the file to avoid locking issues
                    shutil.copy(audio_file_path, temp_audio_path)
                    print(f"Created temporary copy of audio file at {temp_audio_path}")
                    
                    # Use the temporary file
                    intro_audio = AudioFileClip(temp_audio_path).with_start(
                        (slides_list[-1]["start_time"]) + (slides_list[-1]["duration"])
                    )
                    list_audios_instance = add_audios(list_audios)
                    list_audios_instance.append(intro_audio)
                    all_clips.append(intro_audio)  # Track for cleanup
                finally:
                    # Clean up temp directory after use
                    try:
                        shutil.rmtree(temp_dir)
                        print(f"Cleaned up temporary directory: {temp_dir}")
                    except Exception as cleanup_error:
                        print(f"Error cleaning up temporary directory: {str(cleanup_error)}")
        except Exception as e:
            print(f"Error handling intro audio: {str(e)}")
            traceback.print_exc()
            # Continue without this audio
            list_audios_instance = add_audios(list_audios)
        
        # list_audios_instance = []
        ### start body process ###
        path = body(body_list=body_list, clips=list_componant, audio_clips=list_audios_instance, 
                    video_name=video_name, webhook_url=webhook_url, meta_data=meta_data)
        url = settings.MEDIA_URL + path
        payload = {
            "url": url,
            "status": "Done",
            "metadata": meta_data
        }
        try:
            response = requests.post(webhook_url, json=payload)
            print("webhook done!")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending video notification: {e}")
            traceback.print_exc()
            payload = {
                "status": "Failed",
                "metadata": meta_data
            }
            requests.post(webhook_url, json=payload)
            print(f"An error occurred while sending video notification: {e}")
        
        b = is_last_task()
    except Exception as e:
        payload = {
            "status": "Failed",
            "metadata": meta_data
        }
        try:
            requests.post(webhook_url, json=payload)
        except Exception as webhook_error:
            print(f"Error sending failure webhook: {webhook_error}")
            
        print(f"An error occurred while rendering video due to: {e}")
        traceback.print_exc()
        b = is_last_task()
    finally:
        # Clean up resources
        for clip in all_clips:
            try:
                if hasattr(clip, 'close'):
                    clip.close()
            except Exception as cleanup_error:
                print(f"Error during clip cleanup: {str(cleanup_error)}")

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
def testsss(image_url, text, duration):
    try:
        ## download image ##
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        image_data_copy = BytesIO(image_data.getvalue())
        
        # response = Slide2(image_path=image_data,text=text,start=0,duration=duration)
        # response = Slide1(image_path=image_data,text=text,start=0,duration=duration)
        # response = Slide4(image_path=image_data,text=text,start=0,duration=duration)
        response = Slide3(image_path=image_data_copy, text=text, start=6, duration=duration)
        video = CompositeVideoClip(response, size=(1920, 1080))
        output_path = f"downloads/testslide11234_testy.mp4"
        video.write_videofile(output_path, fps=30)
        
        # Clean up
        image_data.close()
        image_data_copy.close()
    except Exception as e:
        print(f"Error in testsss: {str(e)}")
        traceback.print_exc()
    