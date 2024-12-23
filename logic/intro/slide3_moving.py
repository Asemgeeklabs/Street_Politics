from moviepy import *
from PIL import Image 
import requests
from io import BytesIO

## method for transition from bottom to top smoothly ##
def effect_transition(t, x, y ,total_distance=None , slow_ratio=1):
    # Total distance desired
    if total_distance == None:
        total_distance = y  # For ratio = 1

    # Proportional adjustment factor for all speeds
    base_total = 280 + ((360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 + 70 + 50)*0.3) 
    scale_factor = (total_distance / base_total)

    # Adjust t by the slow_ratio to effectively slow down the motion
    t = t / slow_ratio

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
    elif 6.2 <= t < 6.5:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 + 70) * 0.3) * scale_factor 
        return (x, (y - offset) - (((t - 6.2) * 50 * scale_factor) ))
    else:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 +  70 + 50) * 0.3 ) * scale_factor 
        return (x, y - offset)

## method for transition from right to left smoothly ##
def sliding_move(t, start, y, total_distance=1920):
    # Base total distance for the sliding motion
    base_total = 280 + ((360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 + 70 + 50)*0.3)
    scale_factor = total_distance / base_total  # Adjust scale factor

    if 0 <= t < 2:
        return (start - (t * 140 * scale_factor), y)  # Adjusted initial speed
    elif 2 <= t < 2.3:
        offset = 280 * scale_factor
        return (start - offset - ((t - 2) * 360 * scale_factor), y)
    elif 2.3 <= t < 2.6:
        offset = (280 + 360 * 0.3) * scale_factor
        return (start - offset - ((t - 2.3) * 330 * scale_factor), y)
    elif 2.6 <= t < 2.9:
        offset = (280 + (360 + 330) * 0.3) * scale_factor
        return (start - offset - ((t - 2.6) * 310 * scale_factor), y)
    elif 2.9 <= t < 3.2:
        offset = (280 + (360 + 330 + 310) * 0.3) * scale_factor
        return (start - offset - ((t - 2.9) * 290 * scale_factor), y)
    elif 3.2 <= t < 3.5:
        offset = (280 + (360 + 330 + 310 + 290) * 0.3) * scale_factor
        return (start - offset - ((t - 3.2) * 270 * scale_factor), y)
    elif 3.5 <= t < 3.8:
        offset = (280 + (360 + 330 + 310 + 290 + 270) * 0.3) * scale_factor
        return (start - offset - ((t - 3.5) * 250 * scale_factor), y)
    elif 3.8 <= t < 4.1:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250) * 0.3) * scale_factor
        return (start - offset - ((t - 3.8) * 230 * scale_factor), y)
    elif 4.1 <= t < 4.4:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230) * 0.3) * scale_factor
        return (start - offset - ((t - 4.1) * 210 * scale_factor), y)
    elif 4.4 <= t < 4.7:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210) * 0.3) * scale_factor
        return (start - offset - ((t - 4.4) * 190 * scale_factor), y)
    elif 4.7 <= t < 5:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190) * 0.3) * scale_factor
        return (start - offset - ((t - 4.7) * 170 * scale_factor), y)
    elif 5 <= t < 5.3:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170) * 0.3) * scale_factor
        return (start - offset - ((t - 5) * 150 * scale_factor), y)
    elif 5.3 <= t < 5.6:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150) * 0.3) * scale_factor
        return (start - offset - ((t - 5.3) * 120 * scale_factor), y)
    elif 5.6 <= t < 5.9:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120) * 0.3) * scale_factor
        return (start - offset - ((t - 5.6) * 90 * scale_factor), y)
    elif 5.9 <= t < 6.2:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90) * 0.3) * scale_factor
        return (start - offset - ((t - 5.9) * 70 * scale_factor), y)
    elif 6.2 <= t <= 6.5:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 + 70) * 0.3) * scale_factor
        return (start - offset - ((t - 6.2) * 50 * scale_factor), y)
    else:
        offset = (280 + (360 + 330 + 310 + 290 + 270 + 250 + 230 + 210 + 190 + 170 + 150 + 120 + 90 + 70 + 50) * 0.3) * scale_factor
        return (start - offset, y)

### method to download image by url ###
def download_image(url,filename=None):
    ### path that image saved on it ###
    if filename == None:
        filename = "downloads/red_image_downloaded.jpg"
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the image content to a file
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Image downloaded and saved as {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
    return filename

"""
with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
"""
# ### method of converting image to red RGB ###
def Red_image(path):
    ### download image ###
    # path = download_image(url=path)
    ## download image ##
    # response = requests.get(path)
    # image_data = BytesIO(response.content)
    # Open the image
    image = Image.open(path)
    # Ensure the image is in RGB mode
    image = image.convert("RGB")
    # Split the image into R, G, B channels
    r, g, b = image.split()
    # Create a new image with only the red channel
    # Set the green and blue channels to 0
    red_image = Image.merge("RGB", (r, Image.new("L", r.size, 0), Image.new("L", r.size, 0)))
    output_path = "downloads/red_image.jpg"
    # Save or display the image
    red_image.save(output_path)
    return output_path

def red_image_movement(t):
    return (-400+t*10)

## method for moving bg ##
def bg_move(t,width,height,duration):
    if t < 0 :
        return (1920,"center")
    elif 0 <= t < 1:
        offset = 1920
        return (offset-(t*(width)*0.6),"center")
    elif 1 <= t <= 2:
        offset = 1920-((width)*0.6)
        return (offset-((t-1)*(width)*0.4),"center")
    elif 2 < t <= (duration - 4):
        offset = 1920-((width)*0.6)-((width)*0.4)
        return (offset,"center")
    else:
        offset = 1920-((width)*0.6)-((width)*0.4)
        return effect_transition(t=(t-(duration-4)),x=offset,y=(1080-height)//2,total_distance=1080)

## text moving method ##
def text_moving(t,text_width,text_height,duration):
    if t < 0 :
        return (1920,"center")
    elif 0 <= t < 1:
        offset = 1920
        return (offset-(t*((text_width*0.4)+200)),"center")
    elif 1 <= t <= 7:
        offset = 1920-((text_width)*0.4)-200
        return (offset-((t-1)*(text_width)*0.1),"center")
    elif 7 < t <= (duration-4):
        offset = 1920-(text_width+200)
        return (offset,"center")
    else:
        offset = 1920-(text_width+200)
        return effect_transition(t=(t-(duration-5)),x=offset,y=(1080-text_height)//2,total_distance=1080)

### compination of slide effect then up effect ###
def slide3Trans(t,start, y , x ,duration,horz_distance=1920,vert_distance=None , slow_ratio=1):
    if t <= duration:
        return sliding_move(t=t,start=start,y=y,total_distance=horz_distance)
    else:
        return effect_transition(t=(t-duration),x=x,y=y,total_distance=vert_distance,slow_ratio=slow_ratio)

