from moviepy import *
from PIL import Image
import requests , cv2
import numpy as np
from .EditingOnImage import process_image_height, process_image_width

def Zoom(clip,mode='in',position='center',speed=1):
    fps = clip.fps
    duration = clip.duration
    total_frames = int(duration*fps)
    def main(get_frame,t):
        frame = get_frame(t)
        h,w = frame.shape[:2]
        i = t*fps
        if mode == 'out':
            i = total_frames-i
        zoom = 1+(i*((0.1*speed)/total_frames))
        positions = {'center':[(w-(w*zoom))/2,(h-(h*zoom))/2],
                     'left':[0,(h-(h*zoom))/2],
                     'right':[(w-(w*zoom)),(h-(h*zoom))/2],
                     'top':[(w-(w*zoom))/2,0],
                     'topleft':[0,0],
                     'topright':[(w-(w*zoom)),0],
                     'bottom':[(w-(w*zoom))/2,(h-(h*zoom))],
                     'bottomleft':[0,(h-(h*zoom))],
                     'bottomright':[(w-(w*zoom)),(h-(h*zoom))]}
        tx,ty = positions[position]
        M = np.array([[zoom,0,tx], [0,zoom,ty]])
        frame = cv2.warpAffine(frame,M,(w,h))
        return frame
    return clip.transform(main)

def scaling_image(t,time_to_center):
    if t <= time_to_center:
        return 1
    else:
        return (1 + ((t-time_to_center)*0.025))

def move_image(t, start_pos, center_pos, time_to_ctr, pause_dur, w, h):
    if t <= 0:
        return start_pos
    elif 0 < t <= time_to_ctr:
        new_height = start_pos[1] - (t * (start_pos[1] - center_pos[1]) / time_to_ctr)
        return (start_pos[0], new_height)
    elif time_to_ctr <= t < time_to_ctr + pause_dur:
        return ("center", "center")
    else:
        return (w, h)
    
def move_shadow(t, start_pos, center_pos, time_to_ctr, pause_dur, w, h):
    if t <= 0:
        return start_pos
    elif 0 < t <= time_to_ctr:
        new_height = start_pos[1] - (t * (start_pos[1] - center_pos[1]) / time_to_ctr)
        return (start_pos[0], new_height)
    elif time_to_ctr <= t < time_to_ctr + pause_dur:
        return center_pos
    else:
        return (w, h)

def image_transition(image_path, total_duration, clips, new_start_time, pause_duration, w, h, speed):
    image = Image.open(image_path)
    image_width, image_height = image.size
    if abs(image_width - image_height) > 50:
        if image_height > image_width:
            path , mask_path = process_image_height(image_path, "downloads/processed_image.png", target_height=800)
            image_clip = ImageClip("downloads/processed_image.png").with_duration(pause_duration).with_fps(30)
        else:
            path , mask_path = process_image_width(image_path, "downloads/processed_image.png", target_width=1000)
            image_clip = ImageClip(path).with_duration(pause_duration).with_duration(pause_duration).with_fps(30)
    else:
        path , mask_path = process_image_width(image_path, "downloads/processed_image.png", target_width=800)
        image_clip = ImageClip("downloads/processed_image.png").with_duration(pause_duration).with_fps(30)
    #### define the start and center position ####
    start_position = ("center", 150)
    center_position = ("center", 0)
    ### convert image mask with transparent layer to video ###
    mask = ImageClip(mask_path,is_mask=True).with_duration(pause_duration).with_fps(30)
    animated_mask = Zoom(mask,mode='in',position='center',speed=1)
    animated_mask_path = "downloads/image_mask.mov"  # Set your desired output path
    animated_mask.write_videofile(animated_mask_path , codec="prores_ks" ,preset="4444",fps=30)
    ### convert image with transparent layer to video ###
    animated_image = Zoom(image_clip,mode='in',position='center',speed=1)
    animated_image_path = "downloads/image_transparent.mov"  # Set your desired output path
    animated_image.write_videofile(animated_image_path, codec="prores_ks" ,preset="4444",fps=30)
    # Load the video file
    image_clip = VideoFileClip(animated_image_path,has_mask=True).with_mask(animated_mask) # has_mask=True ensures alpha transparency is handled
    ####################################
    distance_to_center = start_position[1] - center_position[1]
    time_to_center = distance_to_center / speed
    # Bind the current iteration's variables
    animated_image = (
        image_clip
        .with_position(lambda t, sp=start_position, cp=center_position, time_to_ctr=time_to_center,
                        pause_dur=pause_duration,
                         : move_image(t, sp, cp, time_to_ctr, pause_dur, w, h))
        .with_start(new_start_time)
        .with_duration(pause_duration)
    )
    animated_image = animated_image.with_effects([vfx.CrossFadeIn(0.2)])
    ### append image clip to clips list ###
    clips.append(animated_image)

    total_duration += animated_image.duration
    return total_duration, clips

def video_transition(video_path, total_duration, clips, new_start_time, audio_clips, w, h, speed):
    print("entering video transition")
    video_clip = VideoFileClip(video_path)
    pause_duration = video_clip.duration
    # audio clips
    audio = video_clip.audio
    audio = audio.with_start(new_start_time)
    audio_clips.append(audio)
    # Extract the first frame
    frame_width, frame_height = video_clip.w, video_clip.h
    print("enerting process of video" )
    if frame_height > frame_width:
        video_clip = video_clip.resized(height=850)
        frame_width, frame_height = video_clip.w, video_clip.h
        frame_image = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
        frame_image.save("downloads/final_output.png")
        frame_image = "downloads/final_output.png"
        
        process_image_height(frame_image, "downloads/final_output.png", target_height=850)
        frame_image = ImageClip("downloads/final_output.png")
        start_position = (721, (h /2)-300)
        shadow_position = (721-21, start_position[1]-12)
        shadow_center = (721-21, abs((h / 2) - (frame_image.h / 2))-13)
        center_position = (721, abs((h / 2) - (frame_image.h / 2)))
    else:
        video_clip = video_clip.resized(width=1080)
        frame_width, frame_height = video_clip.w, video_clip.h
        frame_image = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
        frame_image.save("downloads/final_output.png")
        frame_image = "downloads/final_output.png"
        process_image_width(frame_image, "downloads/final_output.png", target_width=1080)
        frame_image = ImageClip("downloads/final_output.png")
        start_position = ("center", (h /2)-100)
        shadow_position = (420-21, start_position[1]-12)
        shadow_center = (420 -21, abs((h / 2) - (frame_image.h / 2))-13)
        center_position = ("center", abs((h / 2) - (frame_image.h / 2)))
    distance_to_center = start_position[1] - center_position[1]
    time_to_center = distance_to_center / speed
    print("animating the video")
    # animating shadow
    shadow = ImageClip("downloads/final_output.png")
    animated_shadow = (
    shadow 
    .with_start(new_start_time)
    .with_duration(pause_duration)
    .with_position(lambda t, sp=shadow_position, cp=shadow_center,
                   time_to_ctr=time_to_center, pause_dur=pause_duration:
                   move_shadow(t, sp, cp, time_to_ctr, pause_dur, w, h))
    )
    animated_shadow = animated_shadow.with_effects([vfx.CrossFadeIn(0.2)])
    animated_video = (
    video_clip 
    .with_start(new_start_time)
    .with_duration(pause_duration)
    .with_position(lambda t, sp=start_position, cp=center_position,
                   time_to_ctr=time_to_center, pause_dur=pause_duration:
                   move_shadow(t, sp, cp, time_to_ctr, pause_dur, w, h))
    )
    animated_video = animated_video.with_effects([vfx.CrossFadeIn(0.2)])
    clips.append(animated_shadow)
    clips.append(animated_video)
    print(animated_video.duration)
    total_duration += animated_video.duration
    return total_duration, clips, audio_clips

