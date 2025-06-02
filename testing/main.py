# This example reads the voltage from a LiPo battery connected to Pimoroni Pico LiPo
# and uses this reading to calculate how much charge is left in the battery.
# It then displays the info on the screen of Pico Display (or Pico Display 2.0).
# With Pimoroni Pico LiPo, you can read the battery percentage while it's charging.
# Save this code as main.py on your Pico if you want it to run automatically!

from machine import ADC, Pin, I2C
import time

from ssd1306 import SSD1306_I2C

vsys = ADC(Pin(29))                 # reads the system input voltage
charging = Pin(24, Pin.IN)          # reading GP24 tells us whether or not USB power is connected
conversion_factor = 3 * 3.3 / 65535

full_battery = 4.2                  # reference voltages for a full/empty battery, in volts
empty_battery = 2.8                 # the values could vary by battery size/manufacturer so you might need to adjust them


i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=400000)

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))

for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))



print(i2c.scan())
#i2c.writeto(0x3c, b'\x00\xAE')
print("test")

# Create the SSD1306 OLED object. 
# The display is 128 wide and 64 high, at I2C address 0x3C.
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

      
while True:
    
    oled.fill(0)  
    oled.text("Hello, RP2040!", 0, 0)
    oled.text("I2C Address: 0x3C", 0, 10)
    oled.text("SSD1306 Demo", 0, 20)
    
    # convert the raw ADC read into a voltage, and then a percentage
    voltage = vsys.read_u16() * conversion_factor
    percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100

    
    if charging.value() == 1:         # if it's plugged into USB power...
        oled.text("Charging!", 10, 50)

    oled.text('{:.2f}'.format(voltage) + "v", 5, 30)
    oled.text('{:.0f}%'.format(percentage), 5, 40)
    oled.show()

    time.sleep(0.5)