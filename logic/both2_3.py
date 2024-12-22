from moviepy import *
from moviepy.video.VideoClip import TextClip
from new_rect import DrawRect
from slide3_moving import *
from slide2_methods import *

# Define the video size (width and height) and duration
video_width = 1920
video_height = 1080

def Slide2(image_path,text):
    ## layers for transition ##
    black = ImageClip('input/black.jpg').resized(width=1920).with_start(1).with_position(lambda t : effect_transition(t, x= 0, y=video_height ) ).with_duration(14+2)
    layer1 = ImageClip('input/layer1.png').resized(width=1920).with_start(1).with_position(lambda t : effect_transition(t , x= 0, y=video_height+200)).with_duration(14+2)
    layer2 = ImageClip('input/layer2.png').resized(width=1920).with_start(1+0.5).with_position(lambda t : effect_transition(t, x= 0, y=video_height+300)).with_duration(14+2)
    ### second image ###
    second_image = ImageClip(image_path).resized(width=1920)
    # second_image = ImageClip("input/hh.webp").resized(width=1920)
    second_image = second_image.with_start(1+0.5).with_duration(14+5).with_position(lambda t : second_image_position(t=t,duration=14,x=(get_postition(end_time=13,distance=1920)),y=0)).resized(lambda t : zoom_in_effect(t))
    ## title 2 ##
    second_title = TextClip(
        text=text.upper(),  
        font_size= 35,  
        color='rgb(248,229,229)',      
        font="Helvetica-Bold.ttf", 
        bg_color= None, 
        margin=(10,10) ,
    )
    ## Set the height to 200 and adjust the width proportionally
    second_title = second_title.resized(height=150)
    # First, calculate the position of `second_title` outside of the lambda function
    second_title = second_title.with_position(lambda t : second_title_position(t=t,duration=14,x=((1920-second_title.w)//2),y=(((1080-second_title.h)//2)-100),initial_point=1120,total_distance=1120+(second_title.h // 2)+640)).with_duration(14+6).with_start(1-1)
    ## background color of text 2 ##
    bg_color = ColorClip(size=(1,second_title.h+20), color=(0, 0, 0))
    ### bg color x and y ###
    bg_color = bg_color.resized(lambda t : bg_color_width(t,width=second_title.w+20,height=second_title.h)).with_duration(14+6).with_position(lambda t : second_title_position(t=t,center=True,duration=14,x=((1920-second_title.w+20)//2),y=(((1080-bg_color.h)//2)-110),initial_point=1100,total_distance=1100+650+(bg_color.h // 2))).with_start(1-1)

    return [black,layer1,layer2,second_image,bg_color,second_title]

# ################   slide 3   ##########################
def Slide3(image_path,text):
    slided_image = ImageClip(image_path).resized(height=1080)
    ## first image ##
    slided_image = slided_image.with_position(lambda t :slide3Trans(t,start=1920,y=0,x=0,vert_distance=1080)).with_duration(20).with_start(14)
    ## convert image to red image ##
    second_image_path = Red_image(image_path)
    # ## second red image ##
    red_image = ImageClip(second_image_path).resized(height=1680).with_position(lambda t :slide3Trans(t=t,start=1920+slided_image.w,y=red_image_movement(t=t),x=slided_image.w,vert_distance=1080)).with_duration(20).with_start(14)
    ### transision of layer ###
    layer3 = ImageClip('input/white.png').resized(height=1080).with_position(lambda t : slide3Trans(t=t,start=1920+200,x=0,y=0,horz_distance=1980+400)).with_duration(10-2).with_start(14+2)
    layer4 = ImageClip('input/red.png').resized(height=1080).with_position(lambda t : slide3Trans(t=t,start=1920+500,x=0,y=0,horz_distance=1920+800)).with_duration(14-2).with_start(14+2)
    red_background = ImageClip("input/red_image.jpg").with_position(lambda t : slide3Trans(t=t,start=1920,y=0,x=0,vert_distance=1080)).with_duration(10+5).with_start(14)
    ### text and background ###
    text = TextClip(
        # text="winter is here".upper(),  
        text=text.upper(),  
        font_size= 70,          
        size = (500,200),
        color="white", 
        font="Helvetica-Bold.ttf",
        bg_color=None, 
        margin=(100,10) ,
    )
    text = text.with_position(lambda t: text_moving(t,text.w,text_height=text.h)).with_duration(10+5).with_start(14+5)
    bg_color2 = ColorClip(size=(text.w+400,text.h+50), color=(0, 0, 0))
    bg_color2 = bg_color2.with_position(lambda t :bg_move(t,width=bg_color2.w,height=bg_color2.h)).with_duration(10+5).with_start(14+4)
    #### rectamgular around text ####
    rect = DrawRect(Canvas_size=bg_color2.size , rect_size= text.size).with_duration(10+5).with_start(14+4).with_position(lambda t :bg_move(t,width=bg_color2.w,height=rect.h))
    return [red_background,red_image,layer3,layer4,slided_image,bg_color2,rect,text]


list_slide2 = Slide2(image_path="input/hh.webp",text="Immigration")
list_slide3 = Slide3(image_path="input/oo.jpg",text="winter is here")
## append elements in one list ##
list_slide2.extend(list_slide3)
final_video = CompositeVideoClip(list_slide2,size=(video_width, video_height))
# Write the video to a file
output_file = "output/slide2_def2.mp4"
final_video.write_videofile(output_file, fps=120)
