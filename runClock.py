# Word Clock
#   Jim Rowe
#   2/22/2019

import time

import WorldClock

# get current local time
current = time.time()
clock = WorldClock.WorldClock(time.localtime(current))
clock.print_words()

WorldClock.print_matrix(clock.get_letter_array())
