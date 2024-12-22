from PIL import Image
from .Add_borders import add_borders_and_resize
from .Shadow import add_drop_shadow

# process image function
def process_image(image_path, output_path, target_width=1080):
    # Step 1: Open the image
    image = Image.open(image_path)
    # Step 2: Resize and add borders
    bordered_image = add_borders_and_resize(image, target_width=target_width)
    # Step 3: Apply drop shadow
    final_image = add_drop_shadow(bordered_image, offset=(10, 20), shadow_color=(0, 0, 0, 150), blur_radius=7)
    # Step 4: Save the result
    final_image.save(output_path)
    return final_image