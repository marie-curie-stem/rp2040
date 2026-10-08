print("Hello World!")
import gc
print("Free memory", gc.mem_free(), "bytes")
gc.mem_free()
from microcontroller import cpu
print("CPU Frequency: ", cpu.frequency/1000000, "MHz")
