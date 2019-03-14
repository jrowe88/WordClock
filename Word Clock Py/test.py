
import time

import adafruit_fancyled.adafruit_fancyled as fancy

import adafruit_dotstar as dotstar

# Declare a 6-element RGB rainbow palette
palette = [fancy.CRGB(1.0, 0.0, 0.0),  # Red
           fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
           fancy.CRGB(0.0, 1.0, 0.0),  # Green
           fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
           fancy.CRGB(0.0, 0.0, 1.0),  # Blue
           fancy.CRGB(0.5, 0.0, 0.5)]  # Magenta


def rainbow_cycle(wait, num_pixels, pixels):
    offset = 0
    for j in range(255):
        for i in range(num_pixels):
            # Load each pixel's color from the palette using an offset, run it
            # through the gamma function, pack RGB value and assign to pixel.
            offset = j / 255.0
            color = fancy.palette_lookup(palette, offset + i / num_pixels)
            color = fancy.gamma_adjust(color, brightness=0.50)
            pixels[i] = color.pack()

        pixels.show()
        time.sleep(wait)


# setup board
num_pixels = 11*12
pixels = dotstar.DotStar(
    11, 10, num_pixels, brightness=1, auto_write=False)  # control brightness w/ gamma from FancyLED library


# rainbow
print('starting up')
delay = 15  # seconds
start = time.time()
while time.time() < start + delay:
    rainbow_cycle(0, num_pixels, pixels)


pixels.fill((10, 10, 10))
pixels.show()
