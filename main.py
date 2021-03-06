from cayennelpp import CayenneLPP
import utime, time
import machine
import BME280
import ssd1306
from machine import SoftI2C,SoftSPI
from ulora import TTN, uLoRa
from time import sleep

#led = machine.Pin(5, machine.Pin.OUT)
#led.value(1)
# Refer to device pinout / schematics diagrams for pin details
# heltec

# init ic2 object
i2c = SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))  # heltec 5/4

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)
LORA_DATARATE = "SF12BW125"  # Choose from several available

# From TTN console for device
DEVADDR = bytearray([0x00, 0x00, 0x00, 0x6E])
NWKEY = bytearray([0x00, 0x00, 0x00, 0x2B, 0x7E, 0x15, 0x16, 0xA6, 0x09, 0xCF, 0xAB, 0xF7, 0x15, 0x88, 0x4F, 0x3C])
APP = bytearray([0x00, 0x00, 0x00, 0x2B, 0x7E, 0x15, 0xD2, 0xA6, 0xAB, 0xF7, 0xCF, 0x4F, 0x3C, 0x15, 0x88, 0x09])


TTN_CONFIG = TTN(DEVADDR, NWKEY, APP, country="AS")

FPORT = 1

lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)
# SENSOR
temp = 0
pres = 0
hum = 0

counter = 0

while True:
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    print(temp)
    print(pres)
    print(hum)
    
    oled.fill(0)
    sleep(.5)
    oled.text('ESP32 OLED BME280', 0, 0)
    oled.text(temp, 0, 20)
    oled.text(hum, 60, 20)
    #oled.text(counter, 0, 40)
    oled.show()
    
    c = CayenneLPP()
    c.addTemperature(1, float(temp))  # Add temperature read to channel 1 
    c.addRelativeHumidity(2, float(hum))  # Add relative humidity read to channel 2
    c.addBarometricPressure(3, float(pres)*100)  # Add another temperature read to channel 3
    
    data = c.getBuffer()  # Get bytes
    lora.frame_counter = counter
    lora.send_data(data, len(data), lora.frame_counter)
    time.sleep(30)
    counter += 1
