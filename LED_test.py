import requests
import neopixel
import board
import time


# Configure the LED strip
num_leds = 15
led_pin = board.D18
strip = neopixel.NeoPixel(led_pin, num_leds, bpp=3)     # pixel_order = GRB
max_brightness = int(255 * 0.66)


for pixel in range(0,5):
    strip[pixel] = (100,0,0)




