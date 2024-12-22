from PIL import Image, ImageFilter 
import numpy as np

def add_drop_shadow(image, offset=(10, 10), shadow_color=(0, 0, 0, 128), blur_radius=10):
    original = image.convert("RGBA")
    # Calculate the size of the new image (original + offset + blur)
    width, height = original.size
    total_width = width + abs(offset[0]) + blur_radius * 4
    total_height = height + abs(offset[1]) + blur_radius * 4
    # Create a transparent canvas
    transparent_canvas = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))
    # Create the shadow layer
    shadow = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))
    # Create a radial gradient for fading edges
    gradient = np.zeros((total_height, total_width), dtype=np.uint8)
    center_x = blur_radius * 2 + width // 2
    center_y = blur_radius * 2 + height // 2
    # Fill the gradient with fading opacity
    for y in range(total_height):
        for x in range(total_width):
            # Calculate the distance from the shadow center
            dist_x = abs(x - center_x)
            dist_y = abs(y - center_y)
            distance = max(dist_x - width // 2, dist_y - height // 2)
            # Compute alpha based on the distance
            if distance <= 0:
                alpha = 255  # Fully opaque in the central rectangle
            elif distance < blur_radius:
                alpha = 255 - int(255 * (distance / blur_radius))  # Fade out
            else:
                alpha = 0  # Fully transparent outside blur radius
            gradient[y, x] = alpha
    # Convert the gradient to an Image
    gradient_image = Image.fromarray(gradient, mode='L')
    # Paste the gradient on top of the shadow layer
    shadow.paste(shadow_color, (0, 0), mask=gradient_image)
    # Apply Gaussian blur to the shadow for smooth fading
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    # Composite the shadow onto the transparent canvas
    transparent_canvas = Image.alpha_composite(transparent_canvas, shadow)
    # Paste the original image on top of the shadow
    original_position = (blur_radius * 2 + max(0, -offset[0])-5, blur_radius * 2 + max(0, -offset[1])-13)
    transparent_canvas.paste(original, original_position, mask=original)
    return transparent_canvas