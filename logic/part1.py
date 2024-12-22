from moviepy import *
from moviepy.video.VideoClip import TextClip
from slide1_moving import *

# Define the video size (width and height) and duration
video_width = 1920
video_height = 1080

### audios urls ###
audios = [
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-0-1731342776589.mp3",
    # "https://machine-genius.s3.amazonaws.com/My_Audios/audio-1-1731342768317.mp3",
    # "https://machine-genius.s3.amazonaws.com/My_Audios/audio-4-1731342770427.mp3",
    # "https://machine-genius.s3.amazonaws.com/My_Audios/audio-7-1731342772608.mp3",
]

## audios creating ##
list_audios = add_audios(audios=audios)

################################################
############# function of slide 1 ##############
def Slide1(image_path,duration,height,anchor_point:tuple,text,font_size):
    ## entro red background ##
    intro_bg = ImageClip("input/intro.png").resized(width=3420)
    intro_bg = intro_bg.cropped(x1=0,y1=490,x2=intro_bg.w,y2=(intro_bg.h-132))
    

    intro_bg = intro_bg.with_duration(duration+6.5).with_position(lambda t  : move(t,common_height=((video_height - intro_bg.h) // 2),duration=duration)).with_start(0)
    ## image of back ground ##
    background_image = ImageClip(image_path).resized(height=height).with_position(lambda t : image_move(t,duration=duration,x_start=anchor_point[0],y_start=anchor_point[1])).with_duration(duration+6.5).with_start(0)
    print(f"width image :{background_image.w}")
    print(f"height image :{background_image.h}")
    #### add title text to video ####
    Title = TextClip(
        # text="basha EL Down town!".upper(),  # The text to display
        # font_size= 110,            # Font size
        text=text.upper(),  # The text to display
        font_size= font_size,            # Font size
        color="rgb(248,229,229)",          # Text color
        font="Helvetica-Bold.ttf",      # Font (ensure the font is available on your system)
        bg_color=None,        # Background color
        size=(626, 840)  ,  # Set the size of the clip
        method = 'caption',
        interline= 30,
    )
        
    Title = Title.with_position(lambda t : text_move(t,duration=duration)).with_duration(duration+6.5).with_start(0)
    return [background_image,intro_bg,Title]

## call method 1 ##
list_slide1 = Slide1(image_path="input/ll.jpeg",height=1180,duration=list_audios[0].duration,anchor_point=(350,200),text="a whirlwind meeting between donald trump and justin trudeau",font_size=63)

final_video = CompositeVideoClip(list_slide1,size=(video_width, video_height))
## compine audios ##
# audio_track = CompositeAudioClip(list_audios)
# final_video = final_video.with_audio(audio_track)
# Write the video to a file
output_file = "output/fist_test1.mp4"
final_video.write_videofile(output_file, fps=120)




    # print(background_image.h)
    # print(background_image.w)