from moviepy import VideoFileClip, ImageClip, CompositeVideoClip 
from .edit_image import process_image
from .Video_Edit import process_video_frame_by_frame
from .FadingIn import fading_with_background
from .Rebeat_background import repeat_video
from datetime import datetime

### initialize background video ###
print(datetime.now())
background_video = VideoFileClip('input/bg_test.mp4')
## get dimensionsof back ground ### 
w, h = background_video.size
## list of pathes of (images / videos ) ##
image_paths = ["input/fl.mp4"]

## speed of clip transision 
speed = 800
## time of clips (images) pause ## 
pause_duration = 7
## initialize a list of combined clips (images / videos ) ##
clips = []
## initialize the total duration of combined clips (images / videos ) ##
total_duration = 0 
## initialize the start time of first clip ##
new_start_time = 0

## looping on clips pathes ##
for i, img_path in enumerate(image_paths):
    if  img_path[-3:] != "mp4":
        process_image(img_path, "final_output.png", target_width=1080)
        image_clip = ImageClip("final_output.png")
        instance_type = "image"
    else:
        print(img_path[-3:])
        process_video_frame_by_frame(img_path,img_path)
        image_clip = VideoFileClip(img_path)
        instance_type = "video"
    ## start point of each clip ##
    start_position = (420, (h /2)-100)
    new_height = start_position[1]
    ## center point of each clip ##
    center_position = (420, abs((h / 2) - (image_clip.h / 2)))
    distance_to_center = start_position[1] - center_position[1] # distance that clip is transmited in 
    ## time clip need to reach center ##
    time_to_center = distance_to_center / speed 
    ## calculate duration for each clip (image / video) ##
    if instance_type == "image":
        instance_duration = time_to_center + pause_duration + 1 ## constant duration
    else:
        instance_duration = image_clip.duration ## self video duration
    ## method to calculate the position of clip according to time (t) ##
    def move_image(t):
        if t < 0: 
            return start_position
        elif 0 <= t <= time_to_center:
            new_height = start_position[1] - (t * (start_position[1] - center_position[1]) / time_to_center)
            return (420, new_height)
        elif time_to_center <= t < time_to_center + pause_duration:
            return center_position
        else:
            return (w, h)
    ## set the duration , start time and postions of clip ##
    animated_image = (
        image_clip
        .with_start(new_start_time)
        .with_duration(instance_duration)
        .with_position(move_image)
    )

    # apply fading function to each clip (video and image) with setting position #
    animated_image = fading_with_background(
        animated_image,
        background_video,
        move_image,
        duration=0.2,
        initial_opacity=0.2
    )
    # append clip to list of clips ##
    clips.append(animated_image)
    new_start_time += instance_duration
    total_duration += animated_image.duration

## modify the duration of background video ##
background_video_repeated = repeat_video(video=background_video,total_duration=total_duration)

final_video = CompositeVideoClip([background_video_repeated] + clips)
final_video.write_videofile("output/ouput19.mp4", fps=30)
print(datetime.now())