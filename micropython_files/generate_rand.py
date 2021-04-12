import machine
import utime
import _thread
import gc
import sdcard
import uos

analog_C0 = machine.ADC(26)
global toWrite_C0

analog_C1 = machine.ADC(27)
global toWrite_C1

rng = []

global core1
global core0
core0 = 1
core1 = 1

led = machine.Pin(25, machine.Pin.OUT)

sd_spi = machine.SPI(1, sck = machine.Pin(10, machine.Pin.OUT), mosi = machine.Pin(11, machine.Pin.OUT), miso = machine.Pin(12, machine.Pin.OUT))
sd = sdcard.SDCard(sd_spi, machine.Pin(9))

uos.mount(sd, "/sd")
print("Mounted")

print("Size: {} MB".format(sd.sectors/2048))

print(uos.listdir("/sd"))

rawName = "sd/rng_data.txt"
rawFile = open(rawName, "w")

def readRNGcore0():
    global toWrite_C0
    global core0
    toWrite_C0 = ""
    read_C0 = analog_C0.read_u16()
    while read_C0 is 0:
        read_C0 = analog_C0.read_u16()
    toWrite_C0 += "{}".format(read_C0)
    toWrite_C0 += "\n"
    core0 += 1
        
def readRNGcore1():
    global toWrite_C1
    global core1
    toWrite_C1 = ""
    read_C1 = analog_C1.read_u16()
    while read_C1 is 0:
        read_C1 = analog_C0.read_u16()
    toWrite_C1 += "{}".format(read_C1)
    toWrite_C1 += "\n"
    core1 += 1

start = utime.ticks_ms()

for i in range(0, 50001):
    _thread.start_new_thread(readRNGcore1, ())
    utime.sleep_ms(1)
    readRNGcore0()
    rng.append(toWrite_C0)
    rng.append(toWrite_C1)
    if i%100 is 0:
        print(i)
    if i%500 is 0 and i is not 0:
        led.value(1)
        print("Writing to file")
        for x in rng:
            rawFile.write(x)
        rawFile.flush()
        print("Flushed")
        rng = []
        utime.sleep_ms(2)
        led.value(0)
    utime.sleep_ms(3)

print("Randomising done")
print("Generated samples:")
print(i*2)
print("Time took [s]:")
stop = utime.ticks_ms()
time = "{}".format(utime.ticks_diff(stop, start)/1000)
print(time)
rawFile.close()
gc.collect()
uos.umount("/sd")
for i in range(0, 6):
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(1)
_thread.exit()