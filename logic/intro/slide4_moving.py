from moviepy import *
import numpy as np

## method to get internal text width ##
def get_internal_text_width(text):
    # Extract the frame (first frame)
    frame = text.get_frame(0)

    # Convert the frame to a binary image (only text pixels)
    # You can choose to threshold the image to focus on non-background pixels
    binary_frame = np.mean(frame, axis=2) > 0.5  # Assumes text is lighter than background

    # Find the bounding box of the text (non-white pixels)
    cols = np.any(binary_frame, axis=0)
    rows = np.any(binary_frame, axis=1)

    # Get the left-most and right-most non-empty columns (text width)
    left = np.argmax(cols)
    right = len(cols) - np.argmax(cols[::-1])

    # The width of the text in pixels
    text_width = right - left
    return text_width

def effect_transition2(t, x, y ,total_distance=None , slow_ratio=1):
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
    

    