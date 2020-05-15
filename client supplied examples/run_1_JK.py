#!/usr/bin/python

fullview.jpg
import digitalio
import board
import time
from PIL import Image, ImageDraw
from IOPi import IOPi
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
bus1 = IOPI(0x20)

import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=0,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
# disp = ili9341.ILI9341(
 #   spi,
 #   rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
   cs=cs_pin,
   dc=dc_pin,
 #   rst=reset_pin,
  #  baudrate=BAUDRATE,
)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
 #   height = disp.width  # we swap height/width to rotate it to landscape!
 #   width = disp.height
#else:
 #   width = disp.width  # we swap height/width to rotate it to landscape!
 #   height = disp.height
# image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
#disp.image(image)



#********** JK COMMENTED OUT BELOW
#GPIO.input([pin])
#GPIO.input([pin])

#if GPIO.input([pin]):
 #   X = 1 

#if GPIO.input([pin]):
 #   X = 2 
#**********

#********** JK ADDED BELOW. MIGHT NEED TO CHANGE RISING TO FALLING AND NEED TO CHANGE NUMBERS TO ACTUAL CHANNEL IDs
GPIO.add_event_detect(1, GPIO.RISING)
GPIO.add_event_detect(2, GPIO.RISING)
GPIO.add_event_detect(3, GPIO.RISING)

i = 1
#************** JK - START LOOP FOR LISTENING TO IO SETTING IMAGE LISTS
while i <= 1:

    if GPIO.event_detected(1):
        xc = 1
    if GPIO.event_detected(2):
        xc = 2
    if GPIO.event_detected(3): 
        xc = 3
        
    if xc == 1:
        image1 = Image.open("/home/pi/Pictures/screen1.png")
        image2 = Image.open("/home/pi/Pictures/screen2.png")
        image3 = Image.open("/home/pi/Pictures/screen3.png")
        image4 = Image.open("/home/pi/Pictures/screen4.png")
        image5 = Image.open("/home/pi/Pictures/screen5.png")
        image6 = Image.open("/home/pi/Pictures/screen6.png")
        image7 = Image.open("/home/pi/Pictures/screen7.png")
        image8 = Image.open("/home/pi/Pictures/screen8.png")
        image9 = Image.open("/home/pi/Pictures/screen9.png")
        image10 = Image.open("/home/pi/Pictures/screen10.png")
        image11 = Image.open("/home/pi/Pictures/screen11.png")
        image12 = Image.open("/home/pi/Pictures/test.png")

    if xc == 2:
        image1 = Image.open("/home/pi/Pictures/screen1.png")
        image2 = Image.open("/home/pi/Pictures/screen1.png")
        image3 = Image.open("/home/pi/Pictures/screen1.png")
        image4 = Image.open("/home/pi/Pictures/screen1.png")
        image5 = Image.open("/home/pi/Pictures/screen1.png")
        image6 = Image.open("/home/pi/Pictures/screen1.png")
        image7 = Image.open("/home/pi/Pictures/screen1.png")
        image8 = Image.open("/home/pi/Pictures/screen1.png")
        image9 = Image.open("/home/pi/Pictures/screen1.png")
        image10 = Image.open("/home/pi/Pictures/screen1.png")
        image11 = Image.open("/home/pi/Pictures/screen1.png")
        image12 = Image.open("/home/pi/Pictures/screen1.png")

    if xc == 3:
        image1 = Image.open("/home/pi/Pictures/screen11.png")
        image2 = Image.open("/home/pi/Pictures/screen11.png")
        image3 = Image.open("/home/pi/Pictures/screen11.png")
        image4 = Image.open("/home/pi/Pictures/screen11.png")
        image5 = Image.open("/home/pi/Pictures/screen11.png")
        image6 = Image.open("/home/pi/Pictures/screen11.png")
        image7 = Image.open("/home/pi/Pictures/screen11.png")
        image8 = Image.open("/home/pi/Pictures/screen11.png")
        image9 = Image.open("/home/pi/Pictures/screen11.png")
        image10 = Image.open("/home/pi/Pictures/screen11.png")
        image11 = Image.open("/home/pi/Pictures/screen11.png")
        image12 = Image.open("/home/pi/Pictures/screen11.png")



    # Scale the image to the smaller screen dimension
    image_ratio = 240 / 240
    screen_ratio = 240 / 240
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = 240
        scaled_height = 240 * 240 // 240
    #image1 = image1.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - 240 // 2
    y = scaled_height // 2 - 240 // 2
    #image1 = image1.crop((x, y, x + 240, y + 240))




    #************** JK COMMENTED OUT BELOW
    #i = 1
    #while i <= 1:
    #*************

    #************** JK - DISPLAY IMAGES WITH SLEEP TIMES
    if xc == 1:
        disp.image(image1)
        time.sleep(2.15)
        disp.image(image2)
        time.sleep(0.17)
        disp.image(image3)
        time.sleep(1.50)
        disp.image(image4)
        time.sleep(0.25)
        disp.image(image5)
        time.sleep(1)
        disp.image(image6)
        time.sleep(.5)
        disp.image(image7)
        time.sleep(.2)
        disp.image(image8)
        time.sleep(.2)
        disp.image(image9)
        time.sleep(.4)
        disp.image(image10)
        time.sleep(.35)
        disp.image(image11)
        time.sleep(1)
        disp.image(image12)
        time.sleep(1)
    
    if xc == 2:
        disp.image(image1)
        time.sleep(3)
        disp.image(image2)
        time.sleep(3)
        disp.image(image3)
        time.sleep(3)
        disp.image(image4)
        time.sleep(3)
        disp.image(image5)
        time.sleep(3)
        disp.image(image6)
        time.sleep(3)
        disp.image(image7)
        time.sleep(3)
        disp.image(image8)
        time.sleep(3)
        disp.image(image9)
        time.sleep(3)
        disp.image(image10)
        time.sleep(3)
        disp.image(image11)
        time.sleep(3)
        disp.image(image12)
        time.sleep(3)
        
    if xc == 3:
        disp.image(image1)
        time.sleep(1)
        disp.image(image2)
        time.sleep(1)
        disp.image(image3)
        time.sleep(1)
        disp.image(image4)
        time.sleep(1)
        disp.image(image5)
        time.sleep(1)
        disp.image(image6)
        time.sleep(1)
        disp.image(image7)
        time.sleep(1)
        disp.image(image8)
        time.sleep(1)
        disp.image(image9)
        time.sleep(1)
        disp.image(image10)
        time.sleep(1)
        disp.image(image11)
        time.sleep(1)
        disp.image(image12)
        time.sleep(1)
        
    i = 1

