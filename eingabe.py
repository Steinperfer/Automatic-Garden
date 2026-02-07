#https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/2
#https://myhydropi.com/connecting-an-electrical-conductivity-sensor-to-a-raspberry-pi/
#https://tutorials-raspberrypi.de/bodenfeuchtigkeit-mit-dem-raspberry-pi-messen/
#import bme280
#import smbus2
from time import sleep
#import spidev
import os
import time

global Lumen, ErdEC, ErdTemp, WasserPH, WasserTemp , LuftHUM , LuftTemp #sensor daten

#### not implimentet sensor
LuftTemp = 16
LuftHUM = 90
WasserTemp = 20
WasserPH = 6.8
ErdTemp = 10
ErdEC = 1.3
Lumen = 800
######


print(LuftHUM, LuftTemp)   #VALUEchecker

def HumTemp():
    port = 1
    address = 0x77 # Adafruit BME280 address. Other BME280s may be different
    bus = smbus2.SMBus(port)
    bme280.load_calibration_params(bus,address)
    while True:
        bme280_data = bme280.sample(bus,address)
        LuftHUM  = bme280_data.humidity
        pressure  = bme280_data.pressure
        LuftTemp = bme280_data.temperature
        print(LuftHUM, pressure, LuftTemp)   #VALUE
        sleep(1)
 