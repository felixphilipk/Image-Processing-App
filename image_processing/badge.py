from PIL import Image, ImageDraw, ImageOps,ImageChops
# from transformers import StableDiffusionPipeline
from diffusers import StableDiffusionPipeline
import numpy as np
import random
import random
import os
import torch



def load_mini_model():
    model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    return model

def  generate_image_fast(model,prompt):
        generated_output = model(prompt=prompt)
        image = generated_output.images[0]
        return image 
 
def change_hue(image, hue):
    """
    Change the hue of an image.
    """
    
    hsv_image = image.convert('HSV')
    
    h, s, v = hsv_image.split()
    
    np_h = np.array(h, dtype=np.uint8)
    np_h += hue
    
    h = Image.fromarray(np_h, 'L')
    
    return Image.merge('HSV', (h, s, v)).convert('RGBA')

def verify_image_and_process_image(uploaded_image):
    """
    Verify the uploaded image and process it to fit into the frame.
    """
    
    frame_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frame.jpg')
    
    frame_image = Image.open(frame_path).convert('RGBA')

    
    random_hue = random.choice(range(0, 360))
    colored_frame = change_hue(frame_image, random_hue)

    
    frame_width, frame_height = colored_frame.size

    radius = frame_width // 4  
    circle_center = (frame_width // 2, frame_height // 2)

   
    uploaded_image = uploaded_image.resize((radius * 2, radius * 2), Image.Resampling.LANCZOS)

  
    mask = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

   
    uploaded_image_with_alpha = Image.new('RGBA', colored_frame.size, (255, 255, 255, 0))
   
    image_position = (circle_center[0] - radius, circle_center[1] - radius)
    uploaded_image_with_alpha.paste(uploaded_image, image_position, mask)

   
    combined = Image.alpha_composite(colored_frame, uploaded_image_with_alpha)

    return combined, random_hue

def generate_image(uploaded_image):
    """
    Verify the generated image and process it to fit into the frame.
    """
    
    frame_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frame.jpg')
    
    frame_image = Image.open(frame_path).convert('RGBA')

    
    random_hue = random.choice(range(0, 360))
    colored_frame = change_hue(frame_image, random_hue)

    
    frame_width, frame_height = colored_frame.size

    radius = frame_width // 4  
    circle_center = (frame_width // 2, frame_height // 2)

   
    uploaded_image = uploaded_image.resize((radius * 2, radius * 2), Image.Resampling.LANCZOS)

  
    mask = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

   
    uploaded_image_with_alpha = Image.new('RGBA', colored_frame.size, (255, 255, 255, 0))
   
    image_position = (circle_center[0] - radius, circle_center[1] - radius)
    uploaded_image_with_alpha.paste(uploaded_image, image_position, mask)

   
    combined = Image.alpha_composite(colored_frame, uploaded_image_with_alpha)

    return combined, random_hue

