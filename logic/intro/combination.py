from intro_methods import *

# Define the video size (width and height) and duration
video_width = 1920
video_height = 1080

### audios urls ###
audios = [
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-0-1731342776589.mp3",
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-1-1731342768317.mp3",
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-4-1731342770427.mp3",
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-7-1731342772608.mp3",
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


################################################
############# function of slide 2 ##############
def Slide2(image_path,text,duration,start):
    ## layers for transition ##
    black = ImageClip('input/black.jpg').resized(width=1920).with_start(start).with_position(lambda t : effect_transition(t, x= 0, y=video_height ) ).with_duration(duration+2)
    layer1 = ImageClip('input/layer1.png').resized(width=1920).with_start(start).with_position(lambda t : effect_transition(t , x= 0, y=video_height+200)).with_duration(duration+2)
    layer2 = ImageClip('input/layer2.png').resized(width=1920).with_start(start+0.5).with_position(lambda t : effect_transition(t, x= 0, y=video_height+300)).with_duration(duration+2)
    ### second image ###
    second_image = ImageClip(image_path).resized(width=1920)
    # second_image = ImageClip("input/hh.webp").resized(width=1920)
    second_image = second_image.with_start(start+0.5).with_duration(duration+8).with_position(lambda t : second_image_position(t=t,duration=duration,x=(get_postition(end_time=list_audios[1].duration,distance=1920)),y=0)).resized(lambda t : zoom_in_effect(t,duration=duration))
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
    second_title = second_title.with_position(lambda t : second_title_position(t=t,duration=duration,x=((1920-second_title.w)//2),y=(((1080-second_title.h)//2)-100),initial_point=1120,total_distance=1120+(second_title.h // 2)+640)).with_duration(duration+6).with_start(start-1)
    ## background color of text 2 ##
    bg_color = ColorClip(size=(1,second_title.h+20), color=(0, 0, 0))
    ### bg color x and y ###
    bg_color = bg_color.resized(lambda t : bg_color_width(t,width=second_title.w+20,height=second_title.h)).with_duration(duration+6).with_position(lambda t : second_title_position(t=t,center=True,duration=duration,x=((1920-(second_title.w+20))//2),y=(((1080-bg_color.h)//2)-110),initial_point=1100,total_distance=1100+650+(bg_color.h // 2))).with_start(start-1)

    return [black,layer1,layer2,second_image,bg_color,second_title]

################################################
############# function of slide 3 ##############
def Slide3(image_path,text,start,duration):
    slided_image = ImageClip(image_path).resized(height=1080)
    ## first image ##
    slided_image = slided_image.with_position(lambda t :slide3Trans(t,duration=duration,start=1920,y=0,x=0,vert_distance=1080)).with_duration(duration+8).with_start(start)
    ## convert image to red image ##
    second_image_path = Red_image(image_path)
    # ## second red image ##
    red_image = ImageClip(second_image_path).resized(height=1680).with_position(lambda t :slide3Trans(t=t,duration=duration,start=1920+slided_image.w,y=red_image_movement(t=t),x=slided_image.w,vert_distance=1080)).with_duration(duration+8).with_start(start)
    ### transision of layer ###
    layer3 = ImageClip('input/white.png').resized(height=1080).with_position(lambda t : slide3Trans(t=t,duration=duration,start=1920+200,x=0,y=0,horz_distance=1980+400)).with_duration(duration-2).with_start(start+2)
    layer4 = ImageClip('input/red.png').resized(height=1080).with_position(lambda t : slide3Trans(t=t,duration=duration,start=1920+500,x=0,y=0,horz_distance=1920+800)).with_duration(duration-2).with_start(start+2)
    # red_background = ImageClip("input/red_image.jpg").with_position(lambda t : slide3Trans(t=t,duration=duration,start=1920,y=0,x=0,vert_distance=1080)).with_duration(duration+5).with_start(start)
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
    text = text.with_position(lambda t: text_moving(t,text.w,text_height=text.h,duration=duration)).with_duration(duration+10).with_start(start+5)
    bg_color2 = ColorClip(size=(text.w+400,text.h+50), color=(0, 0, 0))
    bg_color2 = bg_color2.with_position(lambda t :bg_move(t,width=bg_color2.w,height=bg_color2.h,duration=duration)).with_duration(duration+10).with_start(start+4)
    #### rectamgular around text ####
    rect = DrawRect(Canvas_size=bg_color2.size , rect_size= text.size).with_duration(duration+10).with_start(start+4).with_position(lambda t :bg_move(t,width=bg_color2.w,height=rect.h,duration=duration))
    return [red_image,layer3,layer4,slided_image,bg_color2,rect,text]

################################################
############# function of slide 4 ##############
def Slide4(image_path,text,start,duration):
    gray_background = ColorClip((1920,1080),color=(80,64,64)).with_position(lambda t : effect_transition2(t=t,x=0,y=1080)).with_start(start).with_duration(duration)
    left_layer_gray = ColorClip((640,1080),color=(70,54,53)).with_position(lambda t : effect_transition2(t=t,x=0,y=1480)).with_start(start+1).with_duration(duration)
    middle_layer_gray = ColorClip((640,1080),color=(70,54,53)).with_position(lambda t : effect_transition2(t=t,x=640,y=1880)).with_start(start+1).with_duration(duration)
    right_layer_offwhite = ColorClip((640,1080),color=(254,237,239)).with_position(lambda t : effect_transition2(t=t,x=1280,y=2280)).with_start(start+1).with_duration(duration)
    right_layer_lightgray = ColorClip((640,1080),color=(205,188,187)).with_position(lambda t : effect_transition2(t=t,x=1280,y=3480)).with_start(start+1).with_duration(duration)
    ############ black layers ################
    left_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : effect_transition2(t=t,x=0,y=1880)).with_start(start+2).with_duration(duration)
    middle_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : effect_transition2(t=t,x=640,y=2280)).with_start(start+2).with_duration(duration)
    right_layer_black = ColorClip((640,1080),color=(0,0,0)).with_position(lambda t : effect_transition2(t=t,x=1280,y=4280)).with_start(start+2).with_duration(duration)

    #### divide image 4 to three parts ####
    img4 = ImageClip(image_path).resized(width=1920)
    img4_part1 = img4.cropped(x1=0,y1=0,x2=640,y2=1080).with_position(lambda t : effect_transition2(t=t,x=0,y=2280)).with_start(start+3).with_duration(duration)
    img4_part2 = img4.cropped(x1=640,y1=0,x2=1280,y2=1080).with_position(lambda t : effect_transition2(t=t,x=640,y=2880)).with_start(start+3).with_duration(duration)
    img4_part3 = img4.cropped(x1=1280,y1=0,x2=1920,y2=1080).with_position(lambda t : effect_transition2(t=t,x=1280,y=5280)).with_start(start+3).with_duration(duration)
    ### shadow layers for part 1 , 2  ###
    # create shadow #
    shadow_image = Image.new("RGBA", (640, 1080), (0, 0, 0, 0))
    shadow_video_image = add_drop_shadow(shadow_image, offset=(0, 0), shadow_color=(0, 0, 0, 150), blur_radius=0)
    shadow_video_image.save("shadow_lide4.png")
    # images of shadow #
    shadow1 = ImageClip("shadow_lide4.png").with_position(lambda t : effect_transition2(t=t,x=0,y=2280)).with_start(start+3).with_duration(duration)
    shadow2 = ImageClip("shadow_lide4.png").with_position(lambda t : effect_transition2(t=t,x=640,y=2880)).with_start(start+3).with_duration(duration)
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
    ).with_position(lambda t : effect_transition2(t=t,x=340,y=3180,total_distance=(3180-100),slow_ratio=2.4)).with_start(start).with_duration(duration)

    ## internal text width of text4 ##
    internal_text_width = get_internal_text_width(text=text4)
    #### text color base ####
    text_base_color = ColorClip((internal_text_width,20),color=(170,36,30)).with_position(lambda t : effect_transition2(t=t,x=340,y=3180,total_distance=(3180-(50+text4.h)),slow_ratio=2.5)).with_start(start).with_duration(duration)
    return [gray_background, left_layer_gray,middle_layer_gray,right_layer_offwhite,right_layer_lightgray,left_layer_black,
            middle_layer_black , right_layer_black,img4_part1,img4_part2,img4_part3,shadow1,shadow2,text4,text_base_color]

# ## call method slides ##
list_slide1 = Slide1(image_path="input/ll.jpeg",height=1280,duration=list_audios[0].duration,anchor_point=(350,300),text="a whirlwind meeting between donald trump and justin trudeau",font_size=63)
list_slide2 = Slide2(image_path="input/hh.webp",text="Immigration",duration=list_audios[1].duration,start=list_audios[0].duration)
list_slide3 = Slide3(image_path="input/oo.jpg",text="winter is here",duration=list_audios[2].duration,start=list_audios[0].duration+list_audios[1].duration)
list_slide4 = Slide4(image_path="input/flag.jpg",text="justice system running on fumes",duration=list_audios[3].duration,start=list_audios[0].duration+list_audios[1].duration+list_audios[2].duration)
#### extend all lists items ####
list_slide1.extend(list_slide2)
list_slide1.extend(list_slide3)
list_slide1.extend(list_slide4)
## append elements in one list ##

intro = VideoFileClip("input/Street_Politics_intro.mov", has_mask=True,target_resolution=(1920,1080)).with_start(list_audios[0].duration+list_audios[1].duration+list_audios[2].duration+list_audios[3].duration-2)
list_slide1.append(intro)
final_video = CompositeVideoClip(list_slide1,size=(video_width, video_height))
### composite audios ###
audio_track = CompositeAudioClip(list_audios)
final_video = final_video.with_audio(audio_track)
## Write the video to a file ##
output_file = "output/test_text4.mp4"
final_video.write_videofile(output_file, fps=60)
