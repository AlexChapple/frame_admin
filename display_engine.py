"""
This is the display engine. It displays stuff onto the screen. It's the main file that will display images and captions to the raspberry pi screen.

Author: Alex A Chapple, 2023
Created: 24/03/23
Updated:

"""

import os 
import logging 
from PIL import Image, ImageDraw, ImageFont
import qrcode 

path = os.path.dirname(__file__) + '/'

def display_image(canvas, image_file, loc, center=False):
    
    """ ---- Paramters -----
    
    epd - display object 
    image_file - file path to the image that needs to be displayed 
    size - size of the image we want to display it at 
    loc - location of the image in the canvas 
    colour - colour of the frame background, default to clear (255) 
    mode - Image mode specified by PIL, default to 1 

    """

    logging.info("initialising display for {}".format(image_file))
    
    # Creates image object
    image_to_show = Image.open(image_file)

    # For the main pictures we want to center the image 
    if loc == 'auto': 
        y_loc = int(((image_to_show.size)[1] - 480) / 2)
        canvas.paste(image_to_show, (0, -y_loc))
    else:
        canvas.paste(image_to_show, loc) # Must be a tuple in this case 

def display_text(canvas, caption, fontsize:int, fill=0, loc=(640, 115), dimensions=(350,152)):
    
    """ ---- Paramters -----
    
    canvas - passes in canvas to draw onto 
    text - the caption to display 
    loc - where the text image will be placed
    font - the font we want to display 
    fill - colour of the text to fill, default is 0 for black I think?

    """

    # Load fonts 
    # font = ImageFont.truetype(path + "Font.ttc", fontsize)
    # font = ImageFont.load_default()       
    font = ImageFont.truetype(path + "Roboto-Regular.ttf", fontsize) 
    W = dimensions[0]
    H = dimensions[1]

    # Create text image canvas 
    text_canvas = Image.new('1', (W, H), 255)
    text_draw = ImageDraw.Draw(text_canvas)

    # Draw text 
    w, h = text_draw.textsize(caption)
    text_draw.text((0,(H-h)/2), text=caption, font=font, fill=fill)

    # rotate the image 
    text_canvas = text_canvas.rotate(90, expand=1)

    # paste onto the draw 
    canvas.paste(text_canvas, loc)


def display_textbox(canvas, text, font, loc:tuple, dimensions:tuple, text_align, bgcolor=255):
    
    """ ----- Parameters -----
    
    canvas - the canvas we want to paste the text onto 
    text - the text we want to display in the box 
    font - the font we want the text to have 
    loc - location where we want to paste the text image 
    dimensions - size of the text image 
    text_align - whether we want the text to be left or center aligned 
    bgcolor - colour of the background, default is white
    
    """

    W, H = dimensions
    image = Image.new('1', dimensions, bgcolor)

    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0,0), text, font=font)

    if text_align == 'center':
        draw.text(((W-w)/2, (H-h)/2), text, font=font, fill='black', align='center')
    elif text_align == "left":
        draw.text((0, (H-h)/2), text, font=font, fill='black', align='left')
    else:
        draw.text((0, (H-h)/2), text, font=font, fill='black', align='left')

    # Rotate the image 
    image = image.rotate(90, expand=1)

    # Paste onto the draw 
    canvas.paste(image, loc)


def draw_box_border(draw, linewidth):
    
    """
    Draws the border around the text and QR code on the frame 
    
    """

    top_left = (637, 5) 
    top_right = (637 + 158, 5)
    bottom_left = (637, 5 + 470) 
    bottom_right = (637 + 158, 5 + 470)
    
    logging.info("drawing box for caption")

    # Drawing box 
    draw.line([top_left, top_right], width=linewidth) 
    draw.line([top_left, bottom_left], width=linewidth)
    draw.line([top_right, bottom_right], width=linewidth)
    draw.line([bottom_left, bottom_right], width=linewidth)



def generate_QR_code(downloadURL, image_path, version=1, box_size=1):
    
    qr = qrcode.QRCode(version=version, box_size=box_size, border=4)

    qr.add_data(downloadURL)

    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # find size of image 
    w, h = qr_img.size

    qr_img.save(image_path)

    return w 


def draw_QR_code(downloadURL, canvas, image_path, loc:tuple, version=1, box_size=1):
    
    w = generate_QR_code(downloadURL, image_path, version=version, box_size=box_size) # Generates a QR code and stores an image 
    qr_code_image = image_path

    # W = 716 
    # H = 25 

    # loc_w = int(W - w/2)
    # loc_h = H 

    display_image(canvas, qr_code_image, loc=loc)


if __name__ == '__main__':

    pass 