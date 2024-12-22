from .intro_methods import *

# test = Slide1(image_path="../input/ll.jpeg",duration=14,text="basha EL Down town!")
test = Slide1(image_path="https://dl.claid.ai/d45ed157-ee05-4956-8788-a7c8263df2ea/CanadaDay-1000x600-1.jpegcls",
                     duration=15,text="elon musk against justin trudeau")

final_video = CompositeVideoClip(test,size=(video_width, video_height))
## Write the video to a file ##
output_file = "../output/testy.mp4"
final_video.write_videofile(output_file, fps=60)

# f = "trudeau family drama"
# print(len(f))
