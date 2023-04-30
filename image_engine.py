"""
Image engine for the picture frame. Turns a picture into its correct size and greyscale

Author: Alex A Chapple, 2023
Created: 15/03/23
Updated:

"""

from PIL import Image, ImageOps
# from pillow_heif import register_heif_opener

def convert_image_to_grayscale(image_file, save=False):
    
    # register_heif_opener()
    
    # Loads image in RGBA 
    gray_image = Image.open(image_file)
    
    # Converts to grayscale using ImageOps function 
    gray_image = ImageOps.grayscale(gray_image)

    # Saves the new image if specified
    if save:
        new_image_name = image_file.split(".")[0]
        gray_image.save("{}_grey.png".format(new_image_name))

    return gray_image


def resize_image(image_name, size, save=False):
    
    # register_heif_opener()

    # Loads image 
    image = Image.open(image_name)

    # Checks to see if photo is landscape or portrait 
    portrait = True 
    image_size = image.size
    if image_size[0] <= image_size[1]:
        portrait = False # if height is less than width, the image is a landscape

     
    # Adjusts image resizing based on landscape or portrait 
    if portrait:
        image.thumbnail(size, Image.LANCZOS)
    else:
        size = size[::-1] # Adjusts cropping to landscape 
        image.thumbnail(size, Image.LANCZOS)

    # Save if required s
    if save:
        new_image_name = image_name.split(".")[0]
        image.save("{}_resized.png".format(new_image_name))

    print("resized image to {}".format(size))

    return image  

def convert_image_to_bmp(image, save=False):
    
    img = Image.open(image)

    # Rotate image for displaying on the screen
    img = rotate_image(img) # Only rotates the image for the bmp file, which is 
                            # only really used for displaying on the frame

    if save:
        img.save("{}.bmp".format(image.replace(".png", "")))
    
    return img 

def rotate_image(img):

    # width, height = img.size

    img = img.rotate(90, expand=1)

    return img 
    
def format_image(image_file, size):
    
    """
        The main function that will re-format the image 
        file for displaying on the frame. 
    """

    convert_image_to_grayscale(image_file, save=True) # Saves a grey scale version of the original image 

    image_file = image_file.replace(".png", "") + "_grey.png"
    # resize_image(image_file, size, save=True) # Resizes the image and rotates if need be 

    # image_file = image_file.replace(".png", "") + "_resized.png"
    img = convert_image_to_bmp(image_file, save=True)

    # Save the image 
    # image_file = image_file.replace("_grey_resized.png", "") + "_formatted.bmp"
    image_file = image_file.replace("_grey.png", "") + "_formatted.bmp"
    img.save(image_file)


### ----- Testing -----

if __name__ == "__main__":

    convert_image_to_grayscale("images/savi.png", save=True)
    resize_image("images/savi_gray.png", (760, 480), save=True)
    convert_image_to_bmp("images/savi_gray_resized.png")

