from .intro_methods import *

# Define the video size (width and height) and duration
video_width = 1920
video_height = 1080

### audios urls ###
audios = [
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-0-1731342776589.mp3",
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-1-1734430317937.mp3",
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-2-1734430315532.mp3",
    "https://machine-genius.s3.amazonaws.com/My_Audios/audio-S4-1734430299637.mp3",
]

## audios creating ##
list_audios = add_audios(audios=audios)

img1 = "https://cdn.britannica.com/87/186687-050-3AA9E551/Justin-Trudeau-2015.jpg"
img2 = "https://www.nationalobserver.com/sites/default/files/styles/scale_width_lg_1x/public/img/2024/12/16/f7ebf4a6-2def-4ae8-b3a6-6537d8c98d33.jpeg?itok=tM4jrEal"
img3 = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Prime_Minister_Trudeau%27s_message_on_Christmas_2023_%280m29s%29_%28cropped%29.jpg/640px-Prime_Minister_Trudeau%27s_message_on_Christmas_2023_%280m29s%29_%28cropped%29.jpg"
img4 = "https://npr.brightspotcdn.com/dims3/default/strip/false/crop/3000x2000+0+0/resize/1100/quality/85/format/jpeg/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F07%2Fe7%2F0fbfaf474dee89c2c5ddbe8694b8%2Fap24351813616898.jpg"

list_slide1 = Slide1(image_path="https://cdn.britannica.com/87/186687-050-3AA9E551/Justin-Trudeau-2015.jpg",
                     duration=list_audios[0].duration,text="elon musk against justin trudeau")
list_slide2 = Slide2(image_path="https://www.nationalobserver.com/sites/default/files/styles/scale_width_lg_1x/public/img/2024/12/16/f7ebf4a6-2def-4ae8-b3a6-6537d8c98d33.jpeg?itok=tM4jrEal",
                     text="Immigration",duration=list_audios[1].duration,start=list_audios[0].duration)
list_slide3 = Slide3(image_path="input/oo.jpg",text="winter is here",duration=list_audios[2].duration,start=list_audios[0].duration+list_audios[1].duration)
list_slide4 = Slide4(image_path="input/flag.jpg",text="justice system running on fumes",duration=list_audios[3].duration,start=list_audios[0].duration+list_audios[1].duration+list_audios[2].duration)
#### extend all lists items ####
list_slide1.extend(list_slide2)
list_slide1.extend(list_slide3)
list_slide1.extend(list_slide4)
## append elements in one list ##
final_video = CompositeVideoClip(list_slide1,size=(video_width, video_height))
### composite audios ###
audio_track = CompositeAudioClip(list_audios)
final_video = final_video.with_audio(audio_track)
## Write the video to a file ##
output_file = "output/sp_canada.mp4"
final_video.write_videofile(output_file, fps=60)

