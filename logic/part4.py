from PIL import Image 
from moviepy import *
from moviepy.video.VideoClip import TextClip
from shadow import add_drop_shadow
from slide4_moving import *

def Slide4(image_path,text):
    gray_background = ColorClip((1920,1080),color=(80,64,64)).with_position(lambda t : effect_transition2(t=t,x=0,y=1080)).with_start(0).with_duration(4+10)
    left_layer_gray = ColorClip((640,1080),color=(70,54,53)).with_position(lambda t : effect_transition2(t=t,x=0,y=1480)).with_start(1).with_duration(4+9)
    middle_layer_gray = ColorClip((640,1080),color=(70,54,53)).with_position(lambda t : effect_transition2(t=t,x=640,y=1880)).with_start(1).with_duration(4+9)
    right_layer_offwhite = ColorClip((640,1080),color=(254,237,239)).with_position(lambda t : effect_transition2(t=t,x=1280,y=2280)).with_start(1).with_duration(4+9)
    right_layer_lightgray = ColorClip((640,1080),color=(205,188,187)).with_position(lambda t : effect_transition2(t=t,x=1280,y=3480)).with_start(1).with_duration(4+9)
    ############ black layers ################
    left_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : effect_transition2(t=t,x=0,y=1880)).with_start(2).with_duration(4+8)
    middle_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : effect_transition2(t=t,x=640,y=2280)).with_start(2).with_duration(4+8)
    right_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : effect_transition2(t=t,x=1280,y=4280)).with_start(2).with_duration(4+8)

    #### divide image 4 to three parts ####
    img4 = ImageClip(image_path).resized(width=1920)
    img4_part1 = img4.cropped(x1=0,y1=0,x2=640,y2=1080).with_position(lambda t : effect_transition2(t=t,x=0,y=2280)).with_start(3).with_duration(4+10)
    img4_part2 = img4.cropped(x1=640,y1=0,x2=1280,y2=1080).with_position(lambda t : effect_transition2(t=t,x=640,y=2880)).with_start(3).with_duration(4+10)
    img4_part3 = img4.cropped(x1=1280,y1=0,x2=1920,y2=1080).with_position(lambda t : effect_transition2(t=t,x=1280,y=5280)).with_start(3).with_duration(4+10)
    ### shadow layers for part 1 , 2  ###
    # create shadow #
    shadow_image = Image.new("RGBA", (640, 1080), (0, 0, 0, 0))
    shadow_video_image = add_drop_shadow(shadow_image, offset=(0, 0), shadow_color=(0, 0, 0, 150), blur_radius=0)
    shadow_video_image.save("shadow_lide4.png")
    # images of shadow #
    shadow1 = ImageClip("shadow_lide4.png").with_position(lambda t : effect_transition2(t=t,x=0,y=2280)).with_start(3).with_duration(4+10)
    shadow2 = ImageClip("shadow_lide4.png").with_position(lambda t : effect_transition2(t=t,x=640,y=2880)).with_start(3).with_duration(4+10)
    ## text 4 ##
    text4 = TextClip(
        # text="justice system running on fumes".upper(),  
        text=text.upper(),  
        font_size= 60,          
        size = (700,300),
        color=(248,229,229), 
        font="Helvetica-Bold.ttf",
        bg_color=None, 
        method = 'caption',
        interline= 30,
        horizontal_align="left",
    ).with_position(lambda t : effect_transition2(t=t,x=340,y=3180,total_distance=(3180-300),slow_ratio=2.4)).with_start(0).with_duration(6+10)

    ## internal text width of text4 ##
    internal_text_width = get_internal_text_width(text=text4)
    #### text color base ####
    text_base_color = ColorClip((internal_text_width,20),color=(170,36,30)).with_position(lambda t : effect_transition2(t=t,x=340,y=3180,total_distance=(3180-(250+text4.h)),slow_ratio=2.5)).with_start(0).with_duration(6+10)
    return [gray_background, left_layer_gray,middle_layer_gray,right_layer_offwhite,right_layer_lightgray,left_layer_black,
            middle_layer_black , right_layer_black,img4_part1,img4_part2,img4_part3,shadow1,shadow2,text4,text_base_color]

list_slide4 = Slide4(image_path="input/flag.jpg",text="justice system running on fumes")
final_video = CompositeVideoClip(list_slide4, size=(1920, 1080))
output_file = "output/slide4_def.mp4"
final_video.write_videofile(output_file, fps=60)


