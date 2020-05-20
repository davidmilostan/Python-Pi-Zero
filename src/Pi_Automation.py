import adafruit_rgb_display.st7789 as st7789
import board
import digitalio
import neopixel
import pygame
import time

from IOPi import IOPi
from PIL import Image, ImageDraw
from .ServoPi import Servo

"""
    The dictionary below contains sets, each set should contain a key "images" and "timing"
    the "images" will contain the path to all the images for that particular set and 
    the "timing" will contain the delay to follow the image
    
    e.g. 
        image_sets["SET_1"]["images"][0] is the path to the first image in set 1
        image_sets["SET_1"]["timing"][0] is the delay that that will come after the first image in set 1 is displayed
"""
image_sets = {
    "SET_1": {
        "images": {
            0: """ SET IMAGE PATH """,
            1: """ SET IMAGE PATH """,
            2: """ SET IMAGE PATH """,
            3: """ SET IMAGE PATH """
        },
        "timing": {
            0: """ SET TIME IN SECONDS """,
            1: """ SET TIME IN SECONDS """,
            2: """ SET TIME IN SECONDS """,
            3: """ SET TIME IN SECONDS """
        }
    },
    "SET_2": {
        "images": {
            0: """ SET IMAGE PATH """,
            1: """ SET IMAGE PATH """,
            2: """ SET IMAGE PATH """,
            3: """ SET IMAGE PATH """
        },
        "timing": {
            0: """ SET TIME IN SECONDS """,
            1: """ SET TIME IN SECONDS """,
            2: """ SET TIME IN SECONDS """,
            3: """ SET TIME IN SECONDS """
        }
    },
    "SET_3": {
        "images": {
            0: """ SET IMAGE PATH """,
            1: """ SET IMAGE PATH """,
            2: """ SET IMAGE PATH """,
            3: """ SET IMAGE PATH """
        },
        "timing": {
            0: """ SET TIME IN SECONDS """,
            1: """ SET TIME IN SECONDS """,
            2: """ SET TIME IN SECONDS """,
            3: """ SET TIME IN SECONDS """
        }
    }
}

"""
    image_set -> image set that is currently being displayed (Default is "SET_1")
    images -> constant key index for the image_sets dictionary
    timing -> constant key index for the image_sets dictionary
"""
image_set = "SET_1"
images = "images"
timing = "timing"

"""
    The two dictionaries below contain rgb colors for the LEDs and brightness values for them
    
    e.g.
        colors["red"] will assign the rgb value of (255, 0, 0)
        brightness["LOW"] will assign value of 0.2 which will change the duty cycle in the neopixel class 
            and therefore adjusting the brightness
"""
colors = {
    "clear": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    'blue': (0, 0, 255)
}
brightness = {
    "OFF": 0,
    "LOW": 0.2,
    "MEDIUM": 0.6,
    "HIGH": 1.0
}

"""
    PIXEL_PIN -> Pin# that the neopixel data line is on
    NUM_PIXELS -> Number of pixels in the strip
    ORDER -> Order for the color tuple "RGB -> (r, g, b) -> (255, 0, 0)" or "GRB -> (g, r, b) -> (0, 255, 0)"
    COLOR -> Value from colors dictionary
    CLEAR -> Value for no color
    button_presses -> Integer value to keep track of how many times the button was pressed to determine brightness
"""
PIXEL_PIN = """ PIN# (RGB LEDs) """
NUM_PIXELS = 4
ORDER = neopixel.RGB
COLOR = colors["red"]
CLEAR = colors["clear"]
led_button_presses = 0

"""
    Dictionary that contains the pin# for each servo data line and
    three different setpoints for each servos angle

    e.g.
        servos["Pin"]["Servo_1] -> Pin number that servo 1 is connected to
        servos["Angles"][Setpoint_2]["Servo_3"] -> The angle servo 3 moves to when the button for the second setpoint is pushed
"""
servos = {
    "Pin": {
        "Servo_1": 1,
        "Servo_2": 7,
        "Servo_3": 15
    },
    "Angles": {
        "Setpoint_1": {
            "Servo_1": """ 0-STEPS """,
            "Servo_2": """ 0-STEPS """,
            "Servo_3": """ 0-STEPS """
        },
        "Setpoint_2": {
            "Servo_1": """ 0-STEPS """,
            "Servo_2": """ 0-STEPS """,
            "Servo_3": """ 0-STEPS """
        },
        "Setpoint_3": {
            "Servo_1": """ 0-STEPS """,
            "Servo_2": """ 0-STEPS """,
            "Servo_3": """ 0-STEPS """
        }
    }
}

""" 
    The move function from Servo class takes 3 arguments
    move(Pin#, Position, Steps)
    
    Pin#: Pin that the data line of the servo is connected to
    Position: Any number between 0-Steps
    Steps: Can be any number between 0-4095
        To increase servo speed decrease number of steps
        To decrease servo speed increase number of steps
"""
STEPS = 250

"""
    The constructor for the Servo class takes 3 arguments
    Servo(Address, Low_Limit, High_Limit)

    Address: Constant of 0x40 if you only have one Servo PWM Pi card
    Low_Limit: Limits the lower bound of rotation for the servo
        If servo does not have full range of motion lower the low limit
        by 0.1 until the servo does not respond anymore
    High_Limit: Limits the higher bound of rotation for the servo
        If the servo does not have a full range of motion increase the high limit
        by 0.1 until the servo does not respond anymore
"""
LOW_LIMIT = 1.0
HIGH_LIMIT = 2.0

"""
    Dictionary that conatains the paths to audio files that are to be played

    e.g.
        audio_files["AUDIO_3"] -> will play the third audio file
"""
audio_files = {
    "AUDIO_1": """ SET AUDIO FILE PATH """,
    "AUDIO_2": """ SET AUDIO FILE PATH """,
    "AUDIO_3": """ SET AUDIO FILE PATH """,
    "AUDIO_4": """ SET AUDIO FILE PATH """,
    "AUDIO_5": """ SET AUDIO FILE PATH """,
    "AUDIO_6": """ SET AUDIO FILE PATH """
}
audio_playing = False

def init_ABE():
    # Create an instance of the IOPi class with an I2C address of 0x20
    iobus = IOPi(0x20)

    # Create an instance of the Servo class with an I2C address of 0x40
    # Servo(Address, Low_Limit, High_Limit)
    # If servo is not getting full range of motion
    #   Decrease low limit by 0.1 until servo does not move
    #   Increase high limit by 0.1 until servo does not move
    servo = Servo(0x40, LOW_LIMIT, HIGH_LIMIT)

    # Setting up input pins 1 = input
    iobus.set_pin_direction(2, 1)
    iobus.set_pin_direction(10, 1)
    iobus.set_pin_direction(16, 1)
    iobus.set_pin_direction(3, 1)
    iobus.set_pin_direction(5, 1)
    iobus.set_pin_direction(6, 1)
    iobus.set_pin_direction(11, 1)
    iobus.set_pin_direction(9, 1)
    iobus.set_pin_direction(14, 1)
    iobus.set_pin_direction(4, 1)

    # Enable servo outputs
    servo.output_enable()

    return iobus, servo

def init_LCD():
    # Configuration for CS and DC pins
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 24000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the display:
    return st7789.ST7789(
        spi,
        height=240,
        y_offset=80,
        rotation=180,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        bauadrate=BAUDRATE
    )

def init_Image(disp):
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width   # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width   # we swap height/width to rotate it to landscape!
        height = disp.height
    
    return Image.new('RGB', (width, height)), width, height

def init_LED():
    # Create an instance of the neopixel class assigning pin number, number of pixels,
    # initial brightness, auto writing rgb value when it changes (if False after pixels.Fill(color) -> pixels.Show() must be done),
    # and the order of the values (RGB, GRB, RGBW, or GRBW)
    pixel = neopixel.NeoPixel(
        PIXEL_PIN,
        NUM_PIXELS,
        brightness=0.0,
        auto_write=True,
        pixel_order=ORDER
    )

    # Initalizing pixels to clear or no color
    pixel.fill(colors["clear"])
    return pixel

def init_Audio():
    pygame.mixer.init()

def scale_Image(image, width, height):
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    return image

def play_Audio(audio):
    # Loads media and plays it
    pygame.mixer.load(audio)
    pygame.mixer.play()

def pause_Audio():
    # Pauses media that is playing
    pygame.mixer.music.pause()

if __name__ == "__main__":
    # Will run the while loop contiuously unitl an error occurs
    # if the error happens to be a keyboard interrupt (Ctrl+C) 
    # the program will end gracefully this is done to give the user
    # a way to end the program without purposly crashing it 
    try:
        # Initialize the expansion boards, the LCD display, image on the LCD, and the LEDs
        iobus, servo = init_ABE()
        disp = init_LCD()
        image, width, height = init_Image(disp)
        pixels = init_LED()
        init_Audio()

        while True:
            # Read each pin that has a button connected to it and determine if one or more of them have been pressed
            if iobus.read_pin(2) == 1:
                # Changes image set to Set 1
                image_set = "SET_1"
            elif iobus.read_pin(10) == 1:
                # Changes image set to Set 2
                image_set = "SET_2"
            elif iobus.read_pin(16) == 1:
                # Changes image set to Set 3
                image_set = "SET_3"
            elif iobus.read_pin(3) == 1:
                # Check to see if the button presses have gone through the 4 press cycle
                # If this is the case reset button_presses to 0 wich is off
                if led_button_presses < 3:
                    led_button_presses += 1
                else:
                    led_button_presses = 0

                if led_button_presses == 0:
                    # Set rgb leds off
                    pixels.brightness = brightness["OFF"]
                    pixels.fill(CLEAR)
                elif led_button_presses == 1:
                    # Set rgb leds intensity level: LOW
                    pixels.brightness = brightness["LOW"]
                    pixels.fill(COLOR)
                elif led_button_presses == 2:
                    # Set rgb leds intensity level: MEDIUM
                    pixels.brightness = brightness["MEDIUM"]
                    pixels.fill(COLOR)
                elif led_button_presses == 3:
                    # Set rgb leds intensity level: HIGH
                    pixels.brightness = brightness["HIGH"]
                    pixels.fill(COLOR)
            elif iobus.read_pin(1) == 1:
                servo.move(servos["Pin"]["Servo_1"], servos["Angles"]["Setpoint_1"]["Servo_1"], STEPS)
                servo.move(servos["Pin"]["Servo_2"], servos["Angles"]["Setpoint_1"]["Servo_2"], STEPS)
                servo.move(servos["Pin"]["Servo_3"], servos["Angles"]["Setpoint_1"]["Servo_3"], STEPS)
            elif iobus.read_pin(7) == 1:
                servo.move(servos["Pin"]["Servo_1"], servos["Angles"]["Setpoint_2"]["Servo_1"], STEPS)
                servo.move(servos["Pin"]["Servo_2"], servos["Angles"]["Setpoint_2"]["Servo_2"], STEPS)
                servo.move(servos["Pin"]["Servo_3"], servos["Angles"]["Setpoint_2"]["Servo_3"], STEPS)
            elif iobus.read_pin(15) == 1:
                servo.move(servos["Pin"]["Servo_1"], servos["Angles"]["Setpoint_3"]["Servo_1"], STEPS)
                servo.move(servos["Pin"]["Servo_2"], servos["Angles"]["Setpoint_3"]["Servo_2"], STEPS)
                servo.move(servos["Pin"]["Servo_3"], servos["Angles"]["Setpoint_3"]["Servo_3"], STEPS)
            elif iobus.read_pin(5) == 1:
                if pygame.mixer.get_busy():
                    pause_Audio()
                else:
                    play_Audio(audio_files["AUDIO_1"])
            elif iobus.read_pin(6) == 1:
                if pygame.mixer.get_busy():
                    pause_Audio()
                else:
                    play_Audio(audio_files["AUDIO_2"])
            elif iobus.read_pin(11) == 1:
                if pygame.mixer.get_busy():
                    pause_Audio()
                else:
                    play_Audio(audio_files["AUDIO_3"])
            elif iobus.read_pin(9) == 1:
                if pygame.mixer.get_busy():
                    pause_Audio()
                else:
                    play_Audio(audio_files["AUDIO_4"])
            elif iobus.read_pin(14) == 1:
                if pygame.mixer.get_busy():
                    pause_Audio()
                else:
                    play_Audio(audio_files["AUDIO_5"])
            elif iobus.read_pin(4) == 1:
                if pygame.mixer.get_busy():
                    pause_Audio()
                else:
                    play_Audio(audio_files["AUDIO_6"])

            # Displays each image in the image set with a delay between each image that is defined in the image_sets dictionary
            delay = 0
            for key, value in image_sets[image_set][images].items():
                image = Image.Open(value)
                image = scale_Image(image, width, height)

                disp.image(image)
                time.sleep(image_sets[image_set][timing][delay])
                delay += 1
    except KeyboardInterrupt:
        # Releases the pin that the neopixel LED is on
        pixels.deinit()
        pass