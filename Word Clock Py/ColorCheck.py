# ColorCheck.py
# Gets a color from an analog input pin
# Maps to HSV hues of 0 to 255
# Supports saturation of 0 to 255
# Returns the color as an RGB value

from console import fg

import board
import RPi.GPIO as GPIO


class ColorCheck:
    def __init__(self, pinInput):
        self._inputPin = pinInput
        self._color = (0, 51, 204)  # a blue
        channel = pinInput
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def color(self):
        return self._color

    def read_color(self):
        val = GPIO.input(channel)

    def read_saturation(self):
        val = GPIO.input(channel)
