from .Add_borders import add_borders_and_resize
from moviepy import VideoFileClip, ImageSequenceClip
from PIL import Image, ImageFilter
import numpy as np
import math 

def add_drop_shadow(image, offset=(5, 5), shadow_color=(0, 0, 0, 128), blur_radius=10):
    """
    Adds a highly blurred drop shadow only to the right and bottom edges of an image.

    Args:
        image (PIL.Image): The input image.
        offset (tuple): Offset of the shadow as (x, y).
        shadow_color (tuple): RGBA color of the shadow.
        blur_radius (int): Radius of Gaussian blur for the shadow.

    Returns:
        PIL.Image: The image with the drop shadow applied.
    """
    original = image.convert("RGBA")
    width, height = original.size

    # Calculate new image dimensions to accommodate shadow and blur
    total_width = width + max(0, offset[0]) 
    total_height = height + max(0, offset[1]) 

    # Create a transparent canvas for the shadow and the image
    transparent_canvas = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # Create a shadow layer
    shadow_layer = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # Define the shadow placement area (right and bottom edges only)
    shadow_box = (
                blur_radius + offset[0] ,  # Extend to width
                blur_radius + offset[1] ,  # Extend to height
                blur_radius + offset[0] + math.ceil(width/2),   # Start at right offset
                blur_radius + offset[1] + math.ceil(height/2)) # Start at bottom offset

    shadow_layer.paste(shadow_color, shadow_box)

    # Apply a strong Gaussian blur for a very diffuse shadow
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))

    # Composite the shadow onto the transparent canvas
    transparent_canvas = Image.alpha_composite(transparent_canvas, shadow_layer)

    # Paste the original image on top of the shadow
    image_position = (blur_radius, blur_radius)
    transparent_canvas.paste(original, image_position, mask=original)

    return transparent_canvas


def add_borders_and_resize(image, target_width=1080):
    """
    Adds borders to an image and resizes it to the target width while maintaining aspect ratio.
    
    Args:
        image (PIL.Image): The input image.
        target_width (int): The desired width of the output image.
    
    Returns:
        PIL.Image: The resized image with borders.
    """
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width

    # Calculate new dimensions
    new_width = target_width
    new_height = int(target_width * aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new image with borders
    border_size = 20
    bordered_width = new_width + border_size * 2
    bordered_height = new_height + border_size * 2
    bordered_image = Image.new("RGBA", (bordered_width, bordered_height), (255, 255, 255, 255))
    bordered_image.paste(resized_image, (border_size, border_size))

    return bordered_image


def process_video_frame_by_frame(input_video_path, output_video_path, target_width=1080):
    """
    Processes a video frame by frame to add borders, resize, and apply a drop shadow.
    
    Args:
        input_video_path (str): Path to the input video.
        output_video_path (str): Path to save the processed video.
        target_width (int): Target width for resizing the video frames.
    """
    # Load the video
    video = VideoFileClip(input_video_path)
    fps = video.fps  # Get frames per second

    processed_frames = []
    for t, frame in video.iter_frames(with_times=True, dtype="uint8"):
        # Convert frame to a PIL image
        frame_image = Image.fromarray(frame)

        # Resize the frame with borders if needed
        bordered_image = add_borders_and_resize(frame_image, target_width=target_width)

        # Adjust shadow transparency for the last frame
        if t < video.duration - 1:
            shadow_color = (0, 0, 0, 0)  # Fully transparent shadow for intermediate frames
        else:
            shadow_color = (0, 0, 0, 150)  # Semi-transparent shadow for the last frame

        # Apply the shadow
        bordered_image_with_shadow = add_drop_shadow(
            bordered_image,
            offset=(5, 5),  # Shadow offset
            shadow_color=shadow_color,
            blur_radius=8  # Adjust shadow spread
        )

        # Convert processed PIL image back to a NumPy array
        processed_frame = np.array(bordered_image_with_shadow)
        processed_frames.append(processed_frame)

    # Create a new video from the processed frames
    processed_video = ImageSequenceClip(processed_frames, fps=fps)
    processed_video.write_videofile(output_video_path, fps=fps)
