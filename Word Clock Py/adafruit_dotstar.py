# The MIT License (MIT)
#
# Copyright (c) 2016 Damien P. George (original Neopixel object)
# Copyright (c) 2017 Ladyada
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# import busio
# import digitalio

START_HEADER_SIZE = 4
LED_START = 0b11100000  # Three "1" bits, followed by 5 brightness bits

# Pixel color order constants
RGB = (0, 1, 2)
RBG = (0, 2, 1)
GRB = (1, 0, 2)
GBR = (1, 2, 0)
BRG = (2, 0, 1)
BGR = (2, 1, 0)


class DotStar:

    def __init__(self, clock, data, n, *, brightness=1.0, auto_write=True,
                 pixel_order=BGR, baudrate=4000000):
        self._spi = None

        self._n = n
        # Supply one extra clock cycle for each two pixels in the strip.

        self._buf = bytearray(n * 4 + START_HEADER_SIZE + 32)
        self.end_header_index = len(self._buf) - 32
        self.pixel_order = pixel_order
        # Four empty bytes to start.
        for i in range(START_HEADER_SIZE):
            self._buf[i] = 0x00
        # Mark the beginnings of each pixel.
        for i in range(START_HEADER_SIZE, self.end_header_index, 4):
            self._buf[i] = 0xff
        # 0xff bytes at the end.
        for i in range(self.end_header_index, len(self._buf)):
            self._buf[i] = 0xff
        self._brightness = 1.0
        # Set auto_write to False temporarily so brightness setter does _not_
        # call show() while in __init__.
        self.auto_write = False
        self.brightness = brightness
        self.auto_write = auto_write

    def deinit(self):
        """Blank out the DotStars and release the resources."""
        self.auto_write = False
        for i in range(START_HEADER_SIZE, self.end_header_index):
            if i % 4 != 0:
                self._buf[i] = 0
        self.show()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def _set_item(self, index, value):

        offset = index * 4 + START_HEADER_SIZE
        rgb = value
        if isinstance(value, int):
            rgb = (value >> 16, (value >> 8) & 0xff, value & 0xff)

        if len(rgb) == 4:
            brightness = value[3]
            # Ignore value[3] below.
        else:
            brightness = 1

        # LED startframe is three "1" bits, followed by 5 brightness bits
        # then 8 bits for each of R, G, and B. The order of those 3 are configurable and
        # vary based on hardware
        # same as math.ceil(brightness * 31) & 0b00011111
        # Idea from https://www.codeproject.com/Tips/700780/Fast-floor-ceiling-functions
        brightness_byte = 32 - int(32 - brightness * 31) & 0b00011111
        self._buf[offset] = brightness_byte | LED_START
        self._buf[offset + 1] = rgb[self.pixel_order[0]]
        self._buf[offset + 2] = rgb[self.pixel_order[1]]
        self._buf[offset + 3] = rgb[self.pixel_order[2]]

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._n)
            length = stop - start
            if step != 0:
                # same as math.ceil(length / step)
                # Idea from https://fizzbuzzer.com/implement-a-ceil-function/
                length = (length + step - 1) // step
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match.")
            for val_i, in_i in enumerate(range(start, stop, step)):
                self._set_item(in_i, val[val_i])
        else:
            self._set_item(index, val)

        if self.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            out = []
            for in_i in range(*index.indices(self._n)):
                out.append(
                    tuple(self._buf[in_i * 4 + (3 - i) + START_HEADER_SIZE] for i in range(3)))
            return out
        if index < 0:
            index += len(self)
        if index >= self._n or index < 0:
            raise IndexError
        offset = index * 4
        return tuple(self._buf[offset + (3 - i) + START_HEADER_SIZE]
                     for i in range(3))

    def __len__(self):
        return self._n

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        self._brightness = min(max(brightness, 0.0), 1.0)
        if self.auto_write:
            self.show()

    def fill(self, color):
        auto_write = self.auto_write
        self.auto_write = False
        for i in range(self._n):
            self[i] = color
        if auto_write:
            self.show()
        self.auto_write = auto_write

    def _ds_writebytes(self, buf):
        for b in buf:
            for _ in range(8):
                b = b << 1

    def show(self):
        # Create a second output buffer if we need to compute brightness
        buf = self._buf
        if self.brightness < 1.0:
            buf = bytearray(self._buf)
            # Four empty bytes to start.
            for i in range(START_HEADER_SIZE):
                buf[i] = 0x00
            for i in range(START_HEADER_SIZE, self.end_header_index):
                buf[i] = self._buf[i] if i % 4 == 0 else int(
                    self._buf[i] * self._brightness)
            # Four 0xff bytes at the end.
            for i in range(self.end_header_index, len(buf)):
                buf[i] = 0xff
