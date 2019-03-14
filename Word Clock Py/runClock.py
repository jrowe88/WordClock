
import configparser
import time

import adafruit_dotstar as dotstar
import board
import rainbow
import WordClock

# Word Clock
#   Jim Rowe
#   2/22/2019

ROWS = 11
COLS = 12

# get value


def read_value(key, defaultValue):
    config = configparser.ConfigParser()
    config.read(['config.ini'])
    if(any(config)):
        default = config['DEFAULT']
        value = default.get(key, defaultValue)
        return value


def write_value(key, value):
    config = configparser.ConfigParser()
    config.read(['config.ini'])
    with open('config.ini', 'w') as configFile:
        config['DEFAULT'][key] = value
        config.write(configFile)


def parseColor(value):
    if(isinstance(value, int)):
        return value
    else:
        # assume it is a hex string
        value = value.lstrip('#')
        value = value.lstrip('0x')
        value = value.lstrip('x')
        return int(value, 16)


# get defaults
configColor = parseColor(read_value('color', '#2889e9'))
pinClock = int(read_value('clockPin', board.SCLK.id))
pinSignal = int(read_value('dataPin', board.MOSI.id))
print('Clock is on pin: ' + str(pinClock))
print('Signal is on pin: ' + str(pinSignal))
print('Color is: ' + str(configColor))

# setup board
num_pixels = ROWS*COLS
pixels = dotstar.DotStar(
    pinClock, pinSignal, num_pixels, brightness=1, auto_write=False)  # control brightness w/ gamma from FancyLED library


# rainbow
print('starting up')
delay = 10  # seconds
start = time.time()
while time.time() < start + delay:
    rainbow.rainbow_cycle(0, num_pixels, pixels)


# run the clock in an indefinite loop
print('running the clock')
previous = 0
while True:
    time.sleep(0.2)
    current = time.time()  # get current local time in seconds
    if(int(current / 60) != int(previous / 60)):  # only update once a minute
        previous = current
        clock = WordClock.WordClock(time.localtime(current), ROWS, COLS)
        clock.print_matrix(clock.get_letter_array())
        clock.print_words()
        clock.copy_to_pixels(
            pixels, configColor, pattern="snake")
        pixels.show()
