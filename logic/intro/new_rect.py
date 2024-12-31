from PIL import Image, ImageDraw
from moviepy import *
import numpy as np

def DrawRect(Canvas_size,rect_size):
    # Parameters
    width, height = Canvas_size  # Canvas size
    rect_width, rect_height = rect_size  # Rectangle dimensions
    # rect_width += 310
    frame_count = 1000  # Total frames for the animation

    # Calculate rectangle coordinates
    # x1 = rect_width
    # x2 = width 
    # y2 = (height - rect_height) // 2
    # y1 = y2 + rect_height
    x1 = width
    x2 = width -rect_width
    y2 = (height - rect_height) // 2
    y1 = y2 + rect_height

    # Create frames
    frames = []
    perimeter = 2 * (rect_width + rect_height)  # Total perimeter of the rectangle

    for frame_number in range(frame_count):
        # Create a blank white canvas
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate progress
        progress = frame_number / (frame_count - 1)
        distance = progress * perimeter  # Current position along the perimeter
        
        # Draw the rectangle in the specified direction
        if distance <= rect_width:
            # Top-right to bottom-right
            draw.line([x1, y1, x1 - int(distance), y1 ], fill=(222,119,122,255), width=5)
        elif distance <= rect_height + rect_width:
            # Bottom-right to bottom-left
            distance -=  rect_width
            draw.line([x1, y1, x2, y1 ], fill=(222,119,122,255), width=5)
            draw.line([x2, y1, x2, y1 - int(distance)], fill=(222,119,122,255), width=5)
        elif distance <= rect_height + (rect_width*2):
            # Bottom-left to top-left
            distance -= rect_height + rect_width
            draw.line([x1, y1, x2, y1 ], fill=(222,119,122,255), width=5)
            draw.line([x2, y1, x2, y2], fill=(222,119,122,255), width=5)
            draw.line([x2, y2, x2 + int(distance), y2 ], fill=(222,119,122,255), width=5)
        else:
            draw.line([x1, y1, x2, y1 ], fill=(222,119,122,255), width=5)
            draw.line([x2, y1, x2, y2], fill=(222,119,122,255), width=5)
            draw.line([x2, y2, x1, y2 ], fill=(222,119,122,255), width=5)
        
        # Append the frame
        frames.append(img)

    # Convert frames to a video with MoviePy
    def make_frame(t):
        # Map time `t` to frame index
        frame_index = int(t * frame_count / duration)
        frame_index = min(frame_index, frame_count - 1)  # Ensure within bounds
        return np.array(frames[frame_index])

    # Create and save video
    duration = 4  # Video duration in seconds
    video_clip = VideoClip(make_frame, duration=duration)
    return video_clip
