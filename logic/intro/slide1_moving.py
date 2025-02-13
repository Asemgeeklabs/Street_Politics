from moviepy import *
import os
import requests

### recursion method for resizing ###
def resize_height_recur(image,current_height):
    image = image.resized(height=current_height+100)
    print(f"new height:{image.h}")
    print(f"new width:{image.w}")
    if image.w < 1920:
        return resize_height_recur(image,(current_height+50))
    else:
        return image

def remove_local_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed local file: {file_path}")
        else:
            print(f"File does not exist: {file_path}")
    except Exception as e:
        print(f"Error removing file {file_path}: {str(e)}")

def add_audios(audios):
    ## audios creating ##
    list_audios = []
    ## looping on all audios ##
    i = 1
    for url , start in audios:
        local_filename = f"downloads/audio{i}.mp3"
        response = requests.get(url, stream=True) 
        response.raise_for_status()  
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  
                file.write(chunk)
        audio = AudioFileClip(local_filename)
        audio = audio.with_start(start)
        list_audios.append(audio)
        print(local_filename)
        i += 1
        remove_local_file(local_filename) 
    return list_audios

# Define the video size (width and height) and duration
video_width = 1920
video_height = 1080
### define speeds of red background movement ##
speed1 = 450
speed2 = 440
speed3 = 430
speed4 = 390
speed5 = 350
speed6 = 330
speed7 = 290
speed8 = 250
speed9 = 200
speed10 = 150
speed11 = 100
#### background image speed ####
background_image_speed = 20
## common height ##
## Define motion function (of comma) to match the video's speed
def effect_transition(t, x, y  ,total_distance=None):
    # Total distance desired
    if total_distance == None:
        total_distance = y  # For ratio = 1

    # Proportional adjustment factor for all speeds
    base_total = 280 + ((360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 + 70 + 50)*0.3) 
    scale_factor = total_distance / base_total 

    if 0 <= t < 2:
        return (x, y - ((t * 140 * scale_factor) ))  # Adjusted initial speed
    elif 2 <= t < 2.3:
        offset = 280 * scale_factor 
        return (x, (y - offset) - (((t - 2) * 360 * scale_factor) ))
    elif 2.3 <= t < 2.6:
        offset = (280 + 360 * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 2.3) * 330 * scale_factor) ))
    elif 2.6 <= t < 2.9:
        offset = (280 + (360 + 330) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 2.6) * 310 * scale_factor) ))
    elif 2.9 <= t < 3.2:
        offset = (280 + (360 + 330 + 310) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 2.9) * 290 * scale_factor) ))
    elif 3.2 <= t < 3.5:
        offset = (280 + (360 + 330 + 310 + 290) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 3.2) * 270 * scale_factor) ))
    elif 3.5 <= t < 3.8:
        offset = (280 + (360 + 330 + 310 + 290 + 270) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 3.5) * 250 * scale_factor) ))
    elif 3.8 <= t < 4.1:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 3.8) * 230 * scale_factor) ))
    elif 4.1 <= t < 4.4:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 4.1) * 210 * scale_factor) ))
    elif 4.4 <= t < 4.7:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 4.4) * 190 * scale_factor) ))
    elif 4.7 <= t < 5:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 4.7) * 170 * scale_factor) ))
    elif 5 <= t < 5.3:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 5) * 150 * scale_factor) ))
    elif 5.3 <= t < 5.6:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 5.3) * 120 * scale_factor) ))
    elif 5.6 <= t < 5.9:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 ) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 5.6) * 90 * scale_factor) ))
    elif 5.9 <= t < 6.2:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 ) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 5.9) * 70 * scale_factor) ))
    elif 6.2 <= t <= 6.5:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 + 70) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 6.2) * 50 * scale_factor) ))
    else:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 +  70 + 50) * 0.3 ) * scale_factor 
        return (x, y - offset)


def move(t,common_height,duration):
    if t <= 0:
        return (0, common_height)  # Start position
    elif 0 < t <= 0.3:
        return (-t * speed1, common_height)  # Smoothly move with speed1
    elif 0.3 < t <= 0.6:
        x_offset = -(speed1*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 0.3) * speed2, common_height)  # Smoothly move with speed2
    elif 0.6 < t <= 0.9:
        x_offset = -(speed1*0.3) -(speed2*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 0.6) * speed3, common_height)  # Smoothly move with speed2
    elif 0.9 < t <= 1.2:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 0.9) * speed4, common_height)  # Smoothly move with speed2
    elif 1.2 < t <= 1.5:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 1.2) * speed5, common_height)  # Smoothly move with speed2
    elif 1.5 < t <= 1.8:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 1.5) * speed6, common_height)  # Smoothly move with speed2
    elif 1.8 < t <= 2.1:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)-(speed6*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 1.8) * speed7, common_height)  # Smoothly move with speed2
    elif 2.1 < t <= 2.4:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)-(speed6*0.3)-(speed7*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 2.1) * speed8, common_height)  # Smoothly move with speed2
    elif 2.4 < t <= 3:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)-(speed6*0.3)-(speed7*0.3)-(speed8*0.3)  # Position reached at t = 0.5
        return (x_offset - (t - 2.4) * speed9, common_height)  # Smoothly move with speed2
    elif 3 < t <= 3.5:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)-(speed6*0.3)-(speed7*0.3)-(speed8*0.3)-(speed9*0.6)  # Position reached at t = 0.5
        return (x_offset - (t - 3) * speed10, common_height)  # Smoothly move with speed2
    elif 3.5 < t <= 4:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)-(speed6*0.3)-(speed7*0.3)-(speed8*0.3)-(speed9*0.6)-(speed10*0.5)   # Position reached at t = 0.5
        return (x_offset - (t - 3.5) * speed11, common_height)  # Smoothly move with speed2
    elif 4 < t <= duration:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)-(speed6*0.3)-(speed7*0.3)-(speed8*0.3)-(speed9*0.6)-(speed10*0.5)-(speed11*0.5) # Position at t = 4
        return (x_offset, common_height)  # Stop moving after t = 4
    elif t > duration:
        x_offset = -(speed1*0.3) -(speed2*0.3)-(speed3*0.3)-(speed4*0.3)-(speed5*0.3)-(speed6*0.3)-(speed7*0.3)-(speed8*0.3)-(speed9*0.6)-(speed10*0.5)-(speed11*0.5) # Position at t = 4
        return effect_transition(t=(t-duration),x=x_offset,y=common_height,total_distance=1080)
    
def image_move(t,duration,x_start,y_start):
    if t <= duration:
        x_offset = x_start
        return (x_offset - ((t) * background_image_speed), -1*(y_start))
    else:
        x_offset = (x_start) - ((t) * background_image_speed)
        return effect_transition(t=(t-duration),x=x_offset,y=(-1*(y_start)),total_distance=1030)

## method of moving text ##
def text_move(t,duration):
    if t < 0:
        return (-656,(video_height/2)-450)
    elif 0 <= t <= 1:
        return (-656+(t*270),(video_height/2)-450)
    elif 1 < t <= 2:
        x_offset = 270
        return (-656+x_offset+((t-1)*220),(video_height/2)-450)
    elif 2 < t <= 3:
        x_offset = 490
        return (-656+x_offset+((t-2)*161),(video_height/2)-450)
    elif 3 < t <= duration:
        return (0,(video_height/2)-450)
    else:
        return effect_transition(t=(t-duration),x=0,y=((video_height/2)-450),total_distance=1080)