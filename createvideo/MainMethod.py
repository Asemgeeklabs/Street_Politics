from logic.intro.intro_methods import *
from logic.content.little.ImageTransition import *
from logic.content.Rebeat_background import repeat_video
import os
import boto3
from datetime import datetime

### list of all slide methods ###
methods_list = [Slide1,Slide2,Slide3,Slide4]

#### body creating method ###
def body(body_list,clips,audio_clips,video_name):
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
            local_filename = f"downloads/video.mp4"

            # Perform the GET request and download the file
            response = requests.get(video_url, stream=True)
            response.raise_for_status()  # Check for HTTP errors
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                    file.write(chunk)
            new_start_time = item["start_time"]
            total_duration, clips, audio_clips = video_transition(local_filename, total_duration, clips, new_start_time, audio_clips, w, h, speed)
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
                image_path = "downloads/content_image.jpg"          
                downloaded_image_path = download_image(url=image_url,filename=image_path)
                total_duration, clips = image_transition(downloaded_image_path, total_duration, clips, new_start_time, image_duration, w, h, speed)
                ### download audio ###
                local_filename = f"downloads/audio.mp3"
                response = requests.get(audioPath, stream=True) 
                response.raise_for_status()  
                with open(local_filename, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):  
                        file.write(chunk)
                audio = AudioFileClip(local_filename).with_start(new_start_time)
                audio_clips.append(audio)
    ## modify the duration of background video ##
    background_video_repeated = repeat_video(video=bg_video, total_duration=total_duration)
    print(f"bacj ground video duration:{background_video_repeated.duration}")
    ### add logo ###
    logo_image = ImageClip("downloads/logo.png").resized(width=150).with_position((1740,20)).with_duration(background_video_repeated.duration).with_start(start_log_bg)
    clips.append(logo_image)
    ### add outro ###
    outro = VideoFileClip("downloads/outro.mp4").with_start(body_list[-1]["start_time"]+body_list[-1]["duration"])
    clips.append(outro)
    video = CompositeVideoClip([background_video_repeated] + clips)
    ### add audio ###
    final_audio = CompositeAudioClip(audio_clips)
    ### add audio to video ###
    video = video.with_audio(final_audio)
    output_path = f"downloads/{video_name}_.mp4"
    video.write_videofile(output_path, fps=30)
    path = upload_to_s3(output_path, f"street_politics/{video_name}")
    return path

def upload_to_s3(file_path, s3_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, os.getenv('AWS_STORAGE_BUCKET_NAME'), s3_path,
                       ExtraArgs={'ACL': 'public-read'})
        print(f"Uploaded {file_path} to S3 bucket.")
        return s3_path
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {str(e)}")

