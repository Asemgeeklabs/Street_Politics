from PIL import Image , ImageOps

def add_borders_and_resize(image, target_width=1080):
    """
    Adds borders and resizes an image.
    Args:
        image (PIL.Image): The input image.
        target_width (int): The target width for resizing.
    Returns:
        PIL.Image: The processed image with borders.
    """
    # Resize the image to the target width, keeping the aspect ratio
    original_width, original_height = image.size
    scale_factor = target_width / original_width
    new_size = (target_width, int(original_height * scale_factor))
    resized_image = image.resize(new_size, Image.LANCZOS)  # Resize using high-quality filter
    
    # Add the first 1px gray border
    border1_color = (169, 169, 169)
    image_with_border1 = ImageOps.expand(resized_image, border=1, fill=border1_color)
    
    # Add the second 10px white border
    border2_color = (255, 255, 255)
    image_with_border2 = ImageOps.expand(image_with_border1, border=10, fill=border2_color)
    
    # Add the third 1px gray border
    image_with_border3 = ImageOps.expand(image_with_border2, border=1, fill=border1_color)
    return image_with_border3