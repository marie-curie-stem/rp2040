import time
import board
import digitalio
import neopixel
import storage

button = digitalio.DigitalInOut(board.BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3

RED = (255, 0, 0)
GREEN = (0, 255, 0)

led[0] = RED

timeout = 5
end = time.monotonic() + timeout

print(f"Press the button in the next {timeout} seconds to enable filesystem writes")

while time.monotonic() < end:
    if not button.value:
        print("Write access activated")
        storage.remount("/", False)
        led[0] = GREEN
        break

    time.sleep(0.01)
else:
    print("Write access NOT activated")

time.sleep(0.5)

import microcontroller
microcontroller.cpu.frequency = 200_000_000
