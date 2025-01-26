from logic.intro.intro_methods import *
from logic.content.little.ImageTransition import *
from logic.content.Rebeat_background import repeat_video
import os , boto3
from logic.content.send_percentage import render_video_with_progress

### list of all slide methods ###
methods_list = [Slide1,Slide2,Slide3,Slide4]

#### body creating method ###
def body(body_list,clips,audio_clips,video_name,webhook_url,meta_data):
    clips2 = []
    ### start of back ground video and logo ###
    start_log_bg = body_list[0]["start_time"]
    print(f"start time logo:{start_log_bg}")
    ### create background video ###
    bg_video = VideoFileClip("downloads/background.mp4")
    w, h = bg_video.size
    speed = 800 
    total_duration = 0
    audio_index = 6
    video_index = 0
    image_index = 1
    for item in body_list:
        try:
            video_url = item["url"]
            local_filename = f"downloads/video{video_index}.mp4"
            ## download vide ##
            if "x.com" in video_url:
                download_twitter_video(url=video_url,output_path=local_filename)
            else:
                # Perform the GET request and download the file
                response = requests.get(video_url, stream=True)
                response.raise_for_status()  # Check for HTTP errors
                with open(local_filename, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                        file.write(chunk)
            new_start_time = item["start_time"]
            total_duration, clips2, audio_clips = video_transition(local_filename, total_duration, clips2, new_start_time, audio_clips, w, h, speed ,video_index)
            video_index += 1
            remove_local_file(local_filename)
        except:
            new_start_time = item["start_time"]
            audioPath = item["audioPath"]
            duration = item["duration"]
            images = item["images"]
            ### download audio ###
            local_filename = f"downloads/audio{audio_index}.mp3"
            response = requests.get(audioPath, stream=True) 
            response.raise_for_status()  
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  
                    file.write(chunk)
            audio = AudioFileClip(local_filename).with_start(new_start_time)
            print(audio_index)
            audio_clips.append(audio)
            audio_index += 1
            remove_local_file(local_filename) # remove file name of audio 
            ## looping on images ##
            for image in images:
                start_time_image = image["pause_duration"]
                image_url = image["url"]
                duration = image["duration"]
                ### download image data ###
                image_path = f"downloads/content_image{image_index}.jpg"          
                downloaded_image_path = download_image(url=image_url,filename=image_path)
                total_duration, clips2 = image_transition(downloaded_image_path, total_duration, clips2, start_time_image, duration , w, h, speed,image_index)
                remove_local_file(downloaded_image_path)
                image_index += 1
    ## modify the duration of background video ##
    print(f"first total duration:{total_duration}")
    background_video_repeated = repeat_video(video=bg_video,total_duration=total_duration).with_start(start_log_bg-1)
    print(f"back ground video duration:{background_video_repeated.duration}")
    print(f"back ground start time :{background_video_repeated.start}")
    clips.insert(-2,background_video_repeated)
    ### add logo ###
    logo_image = ImageClip("downloads/logo.png").resized(width=150).with_position((1740,20)).with_duration(background_video_repeated.duration).with_start(start_log_bg)
    clips2.append(logo_image)
    ### add outro ###
    outro = VideoFileClip("downloads/outro.mp4").with_start(body_list[-1]["start_time"]+body_list[-1]["duration"])
    outro_audio = outro.audio
    outro_audio = outro_audio.with_start((body_list[-1]["start_time"])+(body_list[-1]["duration"]))
    audio_clips.append(outro_audio)
    clips2.append(outro)
    ### APPEND CLIPS of body to clips of intro ###
    clips.extend(clips2)
    video = CompositeVideoClip(clips,size=(1920,1080))
    ### add audio ###
    final_audio = CompositeAudioClip(audio_clips)
    ### add audio to video ###
    # video = video.with_audio(final_audio)
    audio_path = f"downloads/audio_path.mp3"
    final_audio.write_audiofile(audio_path)
    print(f"wrote the final audio")
    output_path = f"downloads/{video_name}.mp4"
    # video.write_videofile(output_path, fps=30)
    ### write video with send percentage to webhock ###
    render_video_with_progress(video,output_path,audio_path,webhook_url=webhook_url,meta_data=meta_data)
    path = upload_to_s3(output_path, f"street_politics/{video_name}.mp4")
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

