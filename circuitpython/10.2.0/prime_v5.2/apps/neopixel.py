# Circuitpython neopixel example 2023/03/12

import time
import board
import neopixel
import digitalio
from rainbowio import colorwheel

pixel_pin  = board.NEOPIXEL
num_pixels = 1

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(wait)
    led.value = not led.value

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

RED    = (255,   0,   0)
YELLOW = (255, 150,   0)
GREEN  = (  0, 255,   0)
CYAN   = (  0, 255, 255)
BLUE   = (  0,   0, 255)
PURPLE = (180,   0, 255)

for i in range(2):
#while True:
    COLORS = [RED, GREEN, BLUE]
    for color in COLORS:
        pixels.fill(color)
        pixels.show()
        led.value = not led.value
        time.sleep(0.5)

    led.value = False
    COLORS2 = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE]
    for color in COLORS2:
        color_chase(color, 0.1)

while True:
    rainbow_cycle(0.002)  # Increase the number to slow down the rainbow
    led.value = not led.value
