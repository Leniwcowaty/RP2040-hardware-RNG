import machine
import utime
import gc
import sdcard
import uos
import urandom
import _thread

global output_1
global output_2

global pp
pp = []

led = machine.Pin(25, machine.Pin.OUT)

sd_spi = machine.SPI(1, sck = machine.Pin(10, machine.Pin.OUT), mosi = machine.Pin(11, machine.Pin.OUT), miso = machine.Pin(12, machine.Pin.OUT))
sd = sdcard.SDCard(sd_spi, machine.Pin(9))

uos.mount(sd, "/sd")
print("Mounted")

print("Size: {} MB".format(sd.sectors/2048))

print(uos.listdir("/sd"))

rawName = "sd/rng_data_60C_Laptop.txt"
rawFile = open(rawName)
ppName = "sd/final_data.txt"
ppFile = open(ppName, "w")

def core0gen():
    global output_1
    output_1 = urandom.getrandbits(16)

def core1gen():
    global output_2
    output_2 = urandom.getrandbits(16)

def scramble(number):
    global pp
    global output_1
    global output_2
    urandom.seed(number)
    for i in range(0, 10):
        _thread.start_new_thread(core1gen, ())
        core0gen()
        scrambledData = "{:0>16}".format(bin(output_1)[2:18]) + "{:0>16}".format(bin(output_2)[2:18])
        toSave = str(int(scrambledData, 2))
        pp.append(toSave)

start = utime.ticks_ms()

i = 0
for lines in rawFile:
    scramble(int(lines))
    i += 1
    if i%50 is 0:
        print(i)
        for lines in pp:
            ppFile.write(lines)
            ppFile.write("\n")
        pp = []
        ppFile.flush()

print("Post-processing done")
print("Time took [s]:")
stop = utime.ticks_ms()
time = "{}".format(utime.ticks_diff(stop, start)/1000)
print(time)

rawFile.close()
ppFile.close()
gc.collect()
uos.umount("/sd")
for i in range(0, 6):
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(1)