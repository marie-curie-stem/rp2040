# toggle the write switch to the local file system 2023/12/14
# increase to 200 MHz, updated to Circuitpython 10.2.0 2026-05-17

import time
import board
import digitalio
import neopixel
import storage

button_pin = board.BUTTON
# T-Display rp2040     board.BUTTON_L    False if pressed
# rp2040 with NeoPixel board.BUTTON
# T-Display ESP32-S2   board.IO0

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
led[0] = RED

time.sleep(1)
timer = 5
can_write = False
print(f"Press the button in the next {timer} seconds to activate saving")
end = time.monotonic() + timer
print(timer)
while end - time.monotonic() > 0:
    if not button.value:
        print("write access activated")
        storage.remount("/", False)
        can_write = True
    if end - timer + 1 < time.monotonic():
        timer -= 1
        led[0] = GREEN
        time.sleep(0.1)
        print(timer)
    if can_write:
        led[0] = GREEN
    else:
        led[0] = RED
print("Not activated")
time.sleep(1)

import microcontroller
microcontroller.cpu.frequency = 200_000_000
