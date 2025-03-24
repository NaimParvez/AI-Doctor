from PIL import Image

def validate_image(image_path):
    try:
        img = Image.open(image_path)
        return img.size[0] > 50 and img.size[1] > 50
    except:
        return False