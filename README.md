# rp2040

Coding examples for the Raspberry Pico 2040.

![GitHub License](https://img.shields.io/github/license/marie-curie-stem/rp2040)
![GitHub Release](https://img.shields.io/github/v/release/marie-curie-stem/rp2040)

## Circuitpython

Here is an old benchmark test with prime numbers, running on Circuitpython 10.2.0 since 2026-05-17. Executed as `code.py`.

``` py
# prime v5.2 2023-12-14 for Raspberry Pico 2040
# cycles through limits and writes to the filesystem
# increase to 200 MHz, updated to Circuitpython 10.2.0 2026-05-17
# https://github.com/marie-curie-stem/rp2040/blob/main/circuitpython/10.2.0/prime_v5.2/code.py

import math, time, digitalio, board, os, neopixel, microcontroller

scope = [100, 1000, 10000, 100000, 1000000, 10000000, 25000000, 100000000, 1000000000, 2147483647, 4294967295]
reference = [25, 168, 1229, 9592, 78498, 664579, 1565927, 5761455, 50847534, 105097564, 203280221]
time_calc = [0, 0, 0, 0, 0, 0, 0, 0, 0]

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
led[0] = RED

def is_prime(number):
    global found
    flag_prime = 1
    for divider in range(3, int(math.sqrt(number)) + 1, 2):
        if number % divider == 0:
            flag_prime = 0
            break
    return flag_prime

def find_primes(largest):
    global primes
    global found
    for number in range(11, largest + 1, 2):
        if is_prime(number) > 0:
            found += 1
            primes.append(number)

def is_prime_fast(number):
    global found
    flag_prime = 1
    largest_divider = int(math.sqrt(number)) + 1
    for divider in primes:
        if number % divider == 0:
            flag_prime = 0
            break
        if divider > largest_divider:
            break
    return flag_prime

def elapsed_time(seconds):
    hours = int(seconds/3600)
    minutes = int(seconds/60 - hours*60)
    sec = int(seconds - minutes*60 - hours*3600)
    return(f"{hours}h {minutes}min {sec}s")

def lightshow():
    for i in range(3141):
        R = abs(255*math.sin(i/100))
        G = abs(255*math.sin((i+105)/100))
        B = abs(255*math.sin((i+210)/100))
        led[0] = (R, G, B)
        time.sleep(0.002)

if __name__ == "__main__":
    lightshow()
    print("New CPU Frequency (MHz):", microcontroller.cpu.frequency / 1_000_000)
    for i in range(len(scope)):
        last = scope[i]
        found = 4              # we start from 11, know 2, 3, 5, 7
        primes = [3, 5, 7]     # exclude 2 since we only test odd numbers
        print(f"\nPrime numbers to {last} in v5.2")
        start = time.monotonic()
        dot = start
        column = 1
        largest_divider = int(math.sqrt(last))
        if largest_divider % 2 == 0:
            largest_divider += 1
        print(f'First find prime dividers up to {largest_divider}.')
        find_primes(largest_divider)
        print(f'Found {found} primes, now use them als dividers.')
        for number in range(largest_divider + 2, last, 2):
            found += is_prime_fast(number)
            if (time.monotonic() - dot) > 2:
                print(".", end="")
                dot = time.monotonic()
                column += 1
                if column % 2 == 0:
                    led[0] = BLUE
                else:
                    led[0] = GREEN
                if column > 30:
                    t = elapsed_time(time.monotonic() - start)
                    print(f" {t} - {number} {int(number*100/last)}% ")
                    column = 1
        duration = time.monotonic() - start
        led[0] = (255, 0, 0)
        print(f'This took: {duration} seconds. {elapsed_time(duration)}')
        print(f'Found {found} primes.')
        filename = "/" + str(last) + ".txt"
        try:
            with open(filename, "w") as fp:
                fp.write(board.board_id)
                fp.write(f'\nPrimes to {last} took {duration} seconds.')
                fp.write(f'\nFound {found} primes. Should be {reference[i]}.')
                print('Exported to filesystem ')
                led[0] = GREEN
        except:
            print("Can't write to the filesystem. Press reset and after that the boot button in the first 5 seconds")
            led[0] = RED
        #print(f'Primes to {last} took {(end - start)} seconds.')
        #print(f'Found {found} primes. Should be {reference[i]}.')
        time_calc[i] = duration
    print('\nWrite summary')
    try:
        with open("summary.txt", "w") as fp:
            fp.write(f'Primes calculation in Circuitpython v5.2 2023/12/11\n')
            fp.write(board.board_id)
            fp.write('\n last       time in seconds\n')
            for i in range(len(time_calc)):
                fp.write(f' {scope[i]}   {time_calc[i]}\n')
            print('Exported to filesystem ')
    except:
        print("Can't write to the filesystem. Press reset and after that the boot button in the first 5 seconds")

while True:
    lightshow()
```

## Arduino C++

Just let the neopixel on pin `board.NEOPIXEL` cycle through the colors.

``` cpp
/* Blink NeoPixel*/
#include <Adafruit_NeoPixel.h>

#define PIN 8

Adafruit_NeoPixel neo(1, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

void setup() {
  neo.begin();
  neo.show();
  Serial.begin(115200);
  delay(1000);
  Serial.println("\nLet's start!");
  Serial.println("Pin used: 8");
}

void loop() {
  neo.setPixelColor(1, 255, 0, 255);
  neo.show();
  delay(2000);
  neo.setPixelColor(1, 0, 255, 255);
  delay(2000);
  neo.show();
  Serial.println("Es geht was.");
}
```
