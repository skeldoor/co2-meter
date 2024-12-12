# sh1107 driver demo code v319
# this code is intended for a 128*128 pixel display

print('starting test')

from machine import Pin, I2C, SoftI2C
import sh1107
print('dir sh1107: ', dir(sh1107))
import gc
import sys
import framebuf
import array
import time

import breakout_scd41
from pimoroni_i2c import PimoroniI2C
from pimoroni import BREAKOUT_GARDEN_I2C_PINS  # or PICO_EXPLORER_I2C_PINS or HEADER_I2C_PINS
import time

from max17048 import MAX17048


i2c = PimoroniI2C(**BREAKOUT_GARDEN_I2C_PINS)  # connect to co2
i2c0 = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000) # connect to screen
display = sh1107.SH1107_I2C(128, 128, i2c0, address=0x3D, rotate=90) # make display

breakout_scd41.init(i2c)
breakout_scd41.start()


devices = i2c.scan()
if devices:
    print("I2C devices found:", [hex(device) for device in devices])
else:
    print("No I2C devices found")



max17048 = MAX17048(i2c)

print("Chip Version:", hex(max17048.get_chip_version()))
print("Cell Voltage:", max17048.get_cell_voltage(), "V")
print("Cell Percentage:", max17048.get_cell_percent(), "%")




while True:
    display.fill(0)
 
    if breakout_scd41.ready():
        co2, temperature, humidity = breakout_scd41.measure()
        print(co2, temperature, humidity)
        display.text('CO2: ' + str(co2), 0, 0, 1)
        display.text('Temp: ' + str(temperature), 0, 8, 1)
        display.text('Humidity: ' + str(humidity), 0, 16, 1)
        display.text('Bat %: ' + str(max17048.get_cell_percent()) + "%", 0, 24, 1)
        display.text('Bat Volts: ' + str(max17048.get_cell_voltage()) + "V", 0, 32, 1)
        display.show()
        time.sleep(5.0)
    else:
        time.sleep(0.5)
        display.text('Waiting...', 0, 0, 1)
        display.show()
        
