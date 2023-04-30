"""

Shows instructions for when the frame is updating on the screen. 
Mainly will be used for device start up.

"""

import sys 
import os 
import logging 
import time 
from PIL import Image, ImageDraw
sys.path.append(os.path.dirname(__file__))

path = os.path.dirname(__file__)
parent = os.path.dirname(path)
sys.path.append(parent)

from display_engine import display_image, display_text
import epd7in5_V2

sys.stdout.flush()

if __name__ == "__main__":

    # Configure the logging 
    logging.basicConfig(level=logging.DEBUG)

    try:
        
        # Initialise the display 
        epd = epd7in5_V2.EPD()
        canvas = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(canvas)

        logging.info("Initialise and clear the canvas")
        epd.init()
        epd.Clear()

        # ----- Load logo ----- 
        logging.info("Display Second")

        image_path = './second.png' 
        display_image(canvas, image_path, loc=(0, 0))

        # ----- Displays everything on screen ----- 
        epd.display(epd.getbuffer(canvas))

        logging.info("Setting display to sleep")
        epd.sleep()

        logging.info("Third displayed successfully")
        time.sleep(3) 
        

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        exit()
