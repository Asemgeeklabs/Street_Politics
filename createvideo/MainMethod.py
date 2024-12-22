from logic.intro.intro_methods import *
from logic.content.little.ImageTransition import *
from logic.content.Rebeat_background import repeat_video
import os
import boto3
from datetime import datetime
# from io import BytesIO
# import requests

### list of all slide methods ###
methods_list = [Slide1,Slide2,Slide3,Slide4]

### method to create intro and content ###
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
        list_audios.append(audio_url)
    list_audios_instance = add_audios(list_audios)
    # final_video = CompositeVideoClip(list_componant,size=(video_width, video_height))
    # mixed_audios = CompositeAudioClip(list_audios_instance)
    # final_video = final_video.with_audio(mixed_audios)
    # ## Write the video to a file ##
    # output_file = "downloads/all_slides.mp4"
    # final_video.write_videofile(output_file, fps=60)
    return list_componant , list_audios_instance 
### method for image editing ###


# #### body creating method ###
# def body(body_list,clips,audio_clips):
#     ### start of back ground video and logo ###
#     start_log_bg = body_list[0]["start_time"]
#     ### create background video ###
#     bg_video = VideoFileClip("downloads/background.mp4").with_start(start_log_bg)
#     w, h = bg_video.size
#     speed = 800 
#     # clips = []
#     # audio_clips = []
#     total_duration = 0
#     for item in body_list:
#         new_start_time = item["start_time"]
#         audioPath = item["audioPath"]
#         duration = item["duration"]
#         images = item["images"]
#         ## duration of each image ##
#         image_duration = duration / len(images)
#         ## looping on images ##
#         number = 1
#         for image in images:
#             print(f"total duration_{number}:{total_duration}")
#             number += 1
#             image_url = image["url"]
#             file_extension = os.path.splitext(image_url)[1].lower()
#             if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
#                 print(f"total_duation :{total_duration}")
#                 image_path = "content_image.jpg"
#                 downloaded_image_path = download_image(url=image_url,filename=image_path)
#                 total_duration, clips = image_transition(downloaded_image_path, total_duration, clips, new_start_time, image_duration, w, h, speed)
#                 audio = AudioFileClip(audioPath).with_start(new_start_time)
#                 audio_clips.append(audio)
#             elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']:
#                 total_duration, clips, audio_clips = video_transition(image_url, total_duration, clips, new_start_time, audio_clips, w, h, speed)
#     print(f"total duration:{total_duration}")
#     ## modify the duration of background video ##
#     background_video_repeated = repeat_video(video=bg_video, total_duration=total_duration)
#     ### add logo ###
#     logo_image = ImageClip("downloads/logo.png").resized(width=150).with_position((1740,20)).with_duration(background_video_repeated.duration).with_start(start_log_bg)
#     clips.append(logo_image)
#     # video = CompositeVideoClip([background_video_repeated] + clips)
#     # ### add audio ###
#     # final_audio = CompositeAudioClip(audio_clips)
#     # ### add audio to video ###
#     # video = video.with_audio(final_audio)
#     # output_path = "downloads/final_endpoint.mp4"
#     # video.write_videofile(output_path, fps=30)
#     # return output_path


#### body creating method ###
def body(body_list,clips,audio_clips):
    ### start of back ground video and logo ###
    start_log_bg = body_list[0]["start_time"]
    ### create background video ###
    bg_video = VideoFileClip("downloads/background.mp4").with_start(start_log_bg)
    w, h = bg_video.size
    speed = 800 
    total_duration = 0
    for item in body_list:
        try:
            video_url = item["url"]
            new_start_time = item["start_time"]
            total_duration, clips, audio_clips = video_transition(video_url, total_duration, clips, new_start_time, audio_clips, w, h, speed)
        except:
            new_start_time = item["start_time"]
            audioPath = item["audioPath"]
            duration = item["duration"]
            images = item["images"]
            ## duration of each image ##
            image_duration = duration / len(images)
            ## looping on images ##
            number = 1
            for image in images:
                print(f"total duration_{number}:{total_duration}")
                number += 1
                image_url = image["url"]
                ### download image data ###
                image_path = "content_image.jpg" 
                
                downloaded_image_path = download_image(url=image_url,filename=image_path)
                total_duration, clips = image_transition(downloaded_image_path, total_duration, clips, new_start_time, image_duration, w, h, speed)
                audio = AudioFileClip(audioPath).with_start(new_start_time)
                audio_clips.append(audio)
    print(f"total duration:{total_duration}")
    ## modify the duration of background video ##
    background_video_repeated = repeat_video(video=bg_video, total_duration=total_duration)
    print(f"bacj ground video duration:{background_video_repeated.duration}")
    ### add logo ###
    logo_image = ImageClip("downloads/logo.png").resized(width=150).with_position((1740,20)).with_duration(background_video_repeated.duration).with_start(start_log_bg)
    clips.append(logo_image)
    # video = CompositeVideoClip([background_video_repeated] + clips)
    # ### add audio ###
    # final_audio = CompositeAudioClip(audio_clips)
    # ### add audio to video ###
    # video = video.with_audio(final_audio)
    # output_path = "downloads/final_endpoint.mp4"
    # video.write_videofile(output_path, fps=30)
    # path = upload_to_s3("downloads/output1.mp4", f"LittleBirdie/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    # return path

def upload_to_s3(file_path, s3_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, os.getenv('AWS_STORAGE_BUCKET_NAME'), s3_path,
                       ExtraArgs={'ACL': 'public-read'})
        print(f"Uploaded {file_path} to S3 bucket.")
        return s3_path
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {str(e)}")

