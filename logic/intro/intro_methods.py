from moviepy import *
from moviepy.video.VideoClip import TextClip
from .new_rect import DrawRect
from .shadow import add_drop_shadow
from .slide1_moving import *
from .slide2_methods import *
from .slide3_moving import *
from .slide4_moving import *

################################################
############# function of slide 1 ##############
def Slide1(image_path,duration,text,start=0,dir_path=None):
    ## entro red background ##
    intro_bg = ImageClip("downloads/intro.png").resized(width=3420)
    intro_bg = intro_bg.cropped(x1=0,y1=490,x2=intro_bg.w,y2=(intro_bg.h-132))

    intro_bg = intro_bg.with_duration(duration+6.5).with_position(lambda t  : move(t,common_height=((video_height - intro_bg.h) // 2),duration=duration)).with_start(0)
    ## image of back ground ##
    background_image = ImageClip(image_path)
    ### check dimintions of image ###
    if background_image.h > background_image.w:
        background_image = background_image.resized(width=1920).with_position(lambda t : image_move(t,duration=duration,x_start=500,y_start=0)).with_duration(duration+6.5).with_start(start).with_fps(60)
    else:
        background_image = background_image.resized(height=1280).with_position(lambda t : image_move(t,duration=duration,x_start=600,y_start=0)).with_duration(duration+6.5).with_start(start).with_fps(60)
    #### add title text to video ####
    # check if text is longest than 25 charachter #
    if len(text) <= 40 :
        font_size = 95
        margin=(90,10,100,10)
    else:
        font_size = 63
        margin=(50,10) 
    Title = TextClip(
        text=text.upper(),  # The text to display
        font_size= font_size,            # Font size
        color="rgb(248,229,229)",          # Text color
        font="downloads/Helvetica-Bold.ttf",      # Font (ensure the font is available on your system)
        bg_color=None,        # Background color
        size=(626, 840)  ,  # Set the size of the clip
        method = 'caption',
        interline= 30,
        margin=margin ,
    )
        
    Title = Title.with_position(lambda t : text_move(t,duration=duration)).with_duration(duration+6.5).with_start(start)
    return [background_image,intro_bg,Title]

################################################
############# function of slide 2 ##############
def Slide2(image_path,text,duration,start,dir_path=None):
    ## layers for transition ##
    black = ImageClip('downloads/black.jpg').resized(width=1920).with_start(start).with_position(lambda t : effect_transition(t, x= 0, y=video_height ) ).with_duration(duration+2)
    layer1 = ImageClip('downloads/layer1.png').resized(width=1920).with_start(start).with_position(lambda t : effect_transition(t , x= 0, y=video_height+200)).with_duration(duration+2)
    layer2 = ImageClip('downloads/layer2.png').resized(width=1920).with_start(start+0.5).with_position(lambda t : effect_transition(t, x= 0, y=video_height+300)).with_duration(duration+2)
    ### second image ###
    # second_image = ImageClip(image_path).resized(width=1920)
    second_image = ImageClip(image_path)
    second_image = resize_height(img=second_image,current_width=1920)
    # second_image = ImageClip("downloads/hh.webp").resized(width=1920)
    second_image = second_image.with_start(start+0.5).with_duration(duration+8).with_position(lambda t : second_image_position(t=t,duration=duration,x=(get_postition(end_time=duration,distance=1920)),y=0)).resized(lambda t : zoom_in_effect(t,duration=duration))
    ## title 2 ##
    # check if text is longest than 25 charachter #
    if len(text) <= 20 :
        font_size = 35
        margin = (20,10)
    else:
        font_size = 20
        margin = (30,10)
    second_title = TextClip(
        text=text.upper(),  
        font_size= font_size,  
        color='rgb(248,229,229)',      
        font="downloads/Helvetica-Bold.ttf", 
        bg_color= None, 
        margin=margin ,
    )
    ## Set the height to 200 and adjust the width proportionally
    second_title = second_title.resized(height=150)
    # First, calculate the position of `second_title` outside of the lambda function
    second_title = second_title.with_position(lambda t : second_title_position(t=t,duration=duration,x=((1920-second_title.w)//2),y=(((1080-second_title.h)//2)-100),initial_point=1120,total_distance=1120+(second_title.h // 2)+640)).with_duration(duration+6).with_start(start-1)
    ## background color of text 2 ##
    bg_color = ColorClip(size=(1,second_title.h+20), color=(0, 0, 0))
    ### bg color x and y ###
    bg_color = bg_color.resized(lambda t : bg_color_width(t,width=second_title.w+20,height=second_title.h)).with_duration(duration+6).with_position(lambda t : second_title_position(t=t,center=True,duration=duration,x=((1920-(second_title.w+20))//2),y=(((1080-bg_color.h)//2)-110),initial_point=1100,total_distance=1100+650+(bg_color.h // 2))).with_start(start-1)

    return [black,layer1,layer2,second_image,bg_color,second_title]

################################################
############# function of slide 3 ##############
def Slide3(image_path,text,start,duration,dir_path=None):
    slided_image = ImageClip(image_path)
    ## convert image to red image ##
    second_image_path = Red_image(image_path,dir_path=dir_path)
    ## first image ##
    if slided_image.w >= slided_image.h: 
        ## resize image ##
        slided_image = slided_image.resized(height=1080)
        ## crop ##
        slided_image = slided_image.cropped(x1=0,y1=0,x2=900,y2=1080)
        slided_image = slided_image.with_position(lambda t :slide3Trans(t,duration=duration,start=1920,y=0,x=0,vert_distance=1080)).with_duration(duration+8).with_start(start)
        # ## second red image ##
        red_image = ImageClip(second_image_path).resized(height=1680).cropped(x1=0,y1=0,x2=1020,y2=1680).with_position(lambda t :slide3Trans(t=t,duration=duration,start=1920+900,y=red_image_movement(t=t),x=900,vert_distance=1080)).with_duration(duration+8).with_start(start)
    else:
        slided_image = slided_image.resized(height=1080).with_position(lambda t :slide3Trans(t,duration=duration,start=1920,y=0,x=0,vert_distance=1080)).with_duration(duration+8).with_start(start)
        # ## second red image ##
        red_image = ImageClip(second_image_path).resized(height=1680).with_position(lambda t :slide3Trans(t=t,duration=duration,start=1920+slided_image.w,y=red_image_movement(t=t),x=slided_image.w,vert_distance=1080)).with_duration(duration+8).with_start(start)
    ### transision of layer ###
    layer3 = ImageClip('downloads/white.png').resized(height=1080).with_position(lambda t : slide3Trans(t=t,duration=duration,start=1920+100,x=0,y=0,horz_distance=1980+400)).with_duration(duration).with_start(start+2)
    layer4 = ImageClip('downloads/red.png').resized(height=1080).with_position(lambda t : slide3Trans(t=t,duration=duration,start=1920+500,x=0,y=0,horz_distance=1920+800)).with_duration(duration).with_start(start+2)
    ### text and background ###
    # check if text is longest than 25 charachter #
    if len(text) <= 23 :
        font_size = 60
        margin = (0,40)
    else:
        font_size = 45
        margin = (0,40)
    Main_text = TextClip(
        text=text.upper(),  
        font_size= font_size,          
        # size = size,
        color="white", 
        font="downloads/Helvetica-Bold.ttf",
        bg_color=None, 
        margin=margin ,
    )
    centered_distance = (1000 - Main_text.w) // 2
    Main_text = Main_text.with_position(lambda t: text_moving(t,Main_text.w,text_height=Main_text.h,duration=(duration-5),centered_distance=centered_distance)).with_duration(duration+10).with_start(start+5)
    # bg_color2 = ColorClip(size=(Main_text.w+400,Main_text.h+50), color=(0, 0, 0))
    bg_color2 = ColorClip(size=(1060,250), color=(0, 0, 0))
    bg_color2 = bg_color2.with_position(lambda t :bg_move(t,width=bg_color2.w,height=bg_color2.h,duration=duration)).with_duration(duration+10).with_start(start+4)
    #### rectamgular around text ####
    # rect = DrawRect(Canvas_size= bg_color2.size , rect_size= Main_text.size).with_duration(duration+10).with_start(start+4).with_position(lambda t :bg_move(t,width=bg_color2.w,height=rect.h,duration=duration))
    rect = DrawRect(Canvas_size= bg_color2.size , rect_size= (1000,200)).with_duration(duration+10).with_start(start+4).with_position(lambda t :bg_move(t,width=bg_color2.w,height=rect.h,duration=duration))
    # rect = DrawRect(Canvas_size= bg_color2.size , rect_size= Main_text.size).with_duration(duration+10).with_start(start+4).with_position(lambda t :bg_move(t,width=bg_color2.w,height=rect.h,duration=duration))
    return [red_image,layer3,layer4,slided_image,bg_color2,rect,Main_text]

################################################
############# function of slide 4 ##############
def Slide4(image_path,text,start,duration,dir_path=None):
    ### check if duration is less than 9 seconds ###
    if duration < 9.5:
        method_motion = effect_transition_fast
        print("fast")
        slow_ratio_text = 1.4
    else:
        method_motion = effect_transition2
        print("slow")
        slow_ratio_text = 2.4


    gray_background = ColorClip((1920,1080),color=(80,64,64)).with_position(lambda t : method_motion(t=t,x=0,y=1080)).with_start(start).with_duration(duration+8)
    left_layer_gray = ColorClip((640,1080),color=(70,54,53)).with_position(lambda t : method_motion(t=t,x=0,y=1480)).with_start(start).with_duration(duration+8)
    middle_layer_gray = ColorClip((640,1080),color=(70,54,53)).with_position(lambda t : method_motion(t=t,x=640,y=1880)).with_start(start).with_duration(duration+8)
    right_layer_offwhite = ColorClip((640,1080),color=(254,237,239)).with_position(lambda t : method_motion(t=t,x=1280,y=2280)).with_start(start).with_duration(duration+8)
    right_layer_lightgray = ColorClip((640,1080),color=(205,188,187)).with_position(lambda t : method_motion(t=t,x=1280,y=3480)).with_start(start).with_duration(duration+8)
    ############ black layers ################
    left_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : method_motion(t=t,x=0,y=1880)).with_start(start).with_duration(duration+8)
    middle_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : method_motion(t=t,x=640,y=2280)).with_start(start).with_duration(duration+8)
    right_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : method_motion(t=t,x=1280,y=4280)).with_start(start).with_duration(duration+8)

    #### divide image 4 to three parts ####
    img4 = ImageClip(image_path)
    ### check if image is landscape ###
    if img4.w > img4.h:
        img4 = resize_height_recur(image=img4,current_height=1030)
    ### image is square or portfolio ###
    else:
        img4 = img4.resized(width=1920)
    ### final point that image stop at ###
    end_height = 1080
    img4_part1 = img4.cropped(x1=0,y1=0,x2=640,y2=end_height).with_position(lambda t : method_motion(t=t,x=0,y=2280)).with_start(start).with_duration(duration+8)
    img4_part2 = img4.cropped(x1=640,y1=0,x2=1280,y2=end_height).with_position(lambda t : method_motion(t=t,x=640,y=2880)).with_start(start).with_duration(duration+8)
    img4_part3 = img4.cropped(x1=1280,y1=0,x2=1920,y2=end_height).with_position(lambda t : method_motion(t=t,x=1280,y=5280)).with_start(start).with_duration(duration+8)
    ### shadow layers for part 1 , 2  ###
    # create shadow #
    shadow_image = Image.new("RGBA", (640, 1080), (0, 0, 0, 0))
    shadow_video_image = add_drop_shadow(shadow_image, offset=(0, 0), shadow_color=(0, 0, 0, 150), blur_radius=0)
    shadow_video_image.save("downloads/shadow_lide4.png")
    # images of shadow #
    shadow1 = ImageClip("downloads/shadow_lide4.png").with_position(lambda t : method_motion(t=t,x=0,y=2280)).with_start(start).with_duration(duration+8)
    shadow2 = ImageClip("downloads/shadow_lide4.png").with_position(lambda t : method_motion(t=t,x=640,y=2880)).with_start(start).with_duration(duration+8)
    ## text 4 ##
    # check if text is longest than 25 charachter #
    if len(text) <= 30 :
        font_size = 95
        margin=(0,0,100,0)
    else:
        font_size = 63
        margin = (80,0,100,0)
    text4 = TextClip(
        # text="justice system running on fumes".upper(),  
        text=text.upper(),  
        font_size= font_size,          
        size = (900,300),
        color=(248,229,229), 
        font="downloads/Helvetica-Bold.ttf",
        bg_color=None, 
        method = 'caption',
        interline= 30,
        horizontal_align="left",
        margin = margin ,
    ).with_position(lambda t : method_motion(t=t,x=340,y=3180,total_distance=(3180-400),slow_ratio=slow_ratio_text)).with_start(start-4).with_duration(duration+6)

    ## internal text width of text4 ##
    internal_text_width = get_internal_text_width(text=text4)
    #### text color base ####
    text_base_color = ColorClip((internal_text_width,20),color=(170,36,30)).with_position(lambda t : method_motion(t=t,x=340,y=3180,total_distance=(3180-(350+text4.h+50)),slow_ratio=slow_ratio_text+0.1)).with_start(start-4).with_duration(duration+6)
    return [gray_background, left_layer_gray,middle_layer_gray,right_layer_offwhite,right_layer_lightgray,left_layer_black,
            middle_layer_black , right_layer_black,img4_part1,img4_part2,img4_part3,shadow1,shadow2,text4,text_base_color]