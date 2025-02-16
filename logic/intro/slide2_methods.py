from moviepy import *
from .slide3_moving import effect_transition , sliding_move

video_height = 1080

## mwthod of zooming image ##
def zoom_in_effect(t, duration,initial_scale=1.0, zoom_rate=0.02):
    if t <= 6.5:
        return initial_scale
    elif 6.5 < t <= duration - 0.5:
        return initial_scale + ((t-6.5) * zoom_rate)
    else:
        return initial_scale + (((duration-0.5)-6.5)*zoom_rate)

# method for second text #
def second_image_position(t,x,y,duration):
    if t <=  duration-0.5:
        return effect_transition(t=t,x="center",y=video_height+600,total_distance=1680)
    else:
        slide_start_time =  duration-0.5
        return sliding_move(
            t=(t - slide_start_time),
            start=x,
            y=y,
        )

# check height of image #
def resize_height(img,current_width):
    img = img.resized(width=current_width)
    if img.h < 1080:
        return resize_height(img,current_width+100)
    else:
        return img

# method for second text moving #
def second_title_position(t,x,y,total_distance,initial_point,duration,center=False):
    if center == True:
        x_effect = "center"
    else:
        x_effect = x
    # Determine the initial position and effect
    if t <=  duration + 1:
        # Perform the `effect_transition` for the duration of the second audio
        return effect_transition(
            t=(t),
            x=x_effect,
            y=video_height+initial_point,
            total_distance=total_distance,
        )
    else:
        slide_start_time =  duration + 1
        return sliding_move(
            t=(t - slide_start_time),
            start=x,
            y=y,
        )
## method of moving background color ##
def bg_color_width(t , width , height):
    if t <= 3 :
        return (1, height+20)  # Ensure width is always at least 1
    elif 3 < t <= 4:
        return (max(1, (((t-3) * 0.05*width)+1)), height+20)
    elif  4 < t <= 6:
        return (max(1, (((t-4) * 0.2*width)+1+(0.05*width))), height+20)
    elif 6 < t <= 8:
        return (max(1, (((t-6) * 0.275*width)+1+(0.05*width)+(width*0.2*2))), height+20)
    else:
        return (1+(0.05*width)+(width*0.2*2)+(0.275*width*2),height+20)
    
### method of calculating new x and y position ###
def get_postition(end_time,distance):
    new_position = -1 * (((((end_time - 7)*0.02))*distance)//2)
    return new_position 
