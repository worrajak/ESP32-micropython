import machine
from machine import Pin, SoftI2C #I2C
import ssd1306
import BME280
from time import sleep

# ESP32 Pin assignment

#i2c = I2C(0)
#i2c = I2C(1, scl=Pin(5), sda=Pin(4), freq=400000)
i2c = SoftI2C(scl=Pin(15), sda=Pin(4), freq=100000)
#i2c = I2C(-1, scl=pyb.Pin.board.PB6, sda=pyb.Pin.board.PB7)

# ESP8266 Pin assignment
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

while True:
  bme = BME280.BME280(i2c=i2c)
  temp = bme.temperature
  hum = bme.humidity
  pres = bme.pressure
  # uncomment for temperature in Fahrenheit
  #temp = (bme.read_temperature()/100) * (9/5) + 32
  #temp = str(round(temp, 2)) + 'F'
  print('Temperature: ', temp)
  print('Humidity: ', hum)
  print('Pressure: ', pres)
  print()
  oled.fill(0)
  sleep(.5)
  oled.text('ESP32 OLED BME280', 0, 0)
  oled.text(temp, 0, 20)
  oled.text(hum, 60, 20)
  oled.show()

  sleep(10)
