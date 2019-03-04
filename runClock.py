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

# setup board
num_pixels = ROWS*COLS
pixels = dotstar.DotStar(
    board.SCLK, board.MOSI, num_pixels, brightness=1, auto_write=False)

# rainbow
delay = 5  # seconds
start = time.time()
while time.time() < start + delay:
    rainbow.rainbow_cycle(0, num_pixels, pixels)

pixels.fill([128, 128, 128])
pixels.show()


# run the clock in an indefinite loop
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
            pixels, [128, 128, 0], pattern="snake")
        # print(pixels)
        pixels.show()
