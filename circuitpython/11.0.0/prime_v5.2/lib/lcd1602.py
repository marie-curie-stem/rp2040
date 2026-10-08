import time
import board
import busio


class LCD:

    def __init__(self, scl=board.GP27, sda=board.GP26, address=0x27):
        self.address = address
        self.i2c = busio.I2C(scl, sda)

        while not self.i2c.try_lock():
            pass

        self._backlight = True
        self._init_lcd()

    def _write(self, value):
        if self._backlight:
            value |= 0x08

        self.i2c.writeto(self.address, bytes([value]))

    def _pulse(self, value):
        self._write(value | 0x04)
        time.sleep(0.000001)
        self._write(value & ~0x04)
        time.sleep(0.0001)

    def _write4(self, value):
        self._write(value)
        self._pulse(value)

    def _command(self, value):
        self._write4(value & 0xF0)
        self._write4((value << 4) & 0xF0)

    def _data(self, value):
        self._write4((value & 0xF0) | 0x01)
        self._write4(((value << 4) & 0xF0) | 0x01)

    def _init_lcd(self):
        time.sleep(0.05)

        self._write4(0x30)
        time.sleep(0.005)

        self._write4(0x30)
        time.sleep(0.001)

        self._write4(0x30)
        time.sleep(0.001)

        self._write4(0x20)

        self._command(0x28)
        self._command(0x0C)
        self._command(0x06)

        self.clear()

    def clear(self):
        self._command(0x01)
        time.sleep(0.002)

    def set_cursor(self, column, row):
        self._command((0x80, 0xC0)[row] + column)

    def write(self, text):
        for char in text:
            self._data(ord(char))

    def message(self, text, line=0):
        self.set_cursor(0, line)
        self.write(text)

    @property
    def backlight(self):
        return self._backlight

    @backlight.setter
    def backlight(self, value):
        self._backlight = bool(value)
        self._write(0)

    def release(self):
        self.i2c.unlock()
