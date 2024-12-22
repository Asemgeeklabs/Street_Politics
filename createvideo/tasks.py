from celery import shared_task
from logic.intro.intro_methods import *
from .MainMethod import body
# from logic.content.Add_borders import add_borders_and_resize
# from logic.content.edit_image import process_image
# from logic.content.Rebeat_background import repeat_video
# from logic.content.Shadow import add_drop_shadow
# from logic.content.Video_Edit import process_video_frame_by_frame

""""
{
                "title": "Canadians Shocked & Disheartened",
                "audioPath": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-S1-1731309711178.mp3",
                "duration": 13.5575,
                "start_time": 0,
                "images": [
                    {
                        "url": "https://dl.claid.ai/d45ed157-ee05-4956-8788-a7c8263df2ea/CanadaDay-1000x600-1.jpeg",
                        "pause_duration": 0
                    }
                ]
            },
"""

### list of all slide methods ###
methods_list = [Slide1,Slide2,Slide3,Slide4]

### method to create intro ###
@shared_task
def intro_create(slides_list):
    list_componant = []
    list_audios = []
    for index , slide in enumerate(slides_list):
        print(f"method index :{methods_list[index]}")
        text = slide["title"]
        audio_url = slide["audioPath"]
        duration = slide["duration"]
        start = slide["start_time"]
        image_url = slide["images"][0]["url"]
        ### create slide content ###
        componant = methods_list[index](image_path=image_url,duration=duration,text=text,start=start)
        list_componant.extend(componant)
        list_audios.append((audio_url,start))
    list_audios_instance = add_audios(list_audios)
    return list_audios_instance , list_componant
    # final_video = CompositeVideoClip(list_componant,size=(video_width, video_height))
    # mixed_audios = CompositeAudioClip(list_audios_instance)
    # final_video = final_video.with_audio(mixed_audios)
    # ## Write the video to a file ##
    # output_file = "downloads/final_test_intro.mp4"
    # final_video.write_videofile(output_file, fps=60)
    # return output_file 

@shared_task
def bodytest(slides_list,body_list):
    list_componant = []
    list_audios = []
    for index , slide in enumerate(slides_list):
        print(f"method index :{methods_list[index]}")
        text = slide["title"]
        audio_url = slide["audioPath"]
        duration = slide["duration"]
        start = slide["start_time"]
        image_url = slide["images"][0]["url"]
        ### create slide content ###
        componant = methods_list[index](image_path=image_url,duration=duration,text=text,start=start)
        list_componant.extend(componant)
        list_audios.append((audio_url,start))
    list_audios_instance = add_audios(list_audios)
    ### start body process ###
    body(body_list=body_list,clips=list_componant,audio_clips=list_audios_instance)

