# ESP32-micropython

  - install anaconda python -> download from website 

  - change firmware -> esp32-idf3-20210202-v1.14.bin to newest file 

  - change com port -> 

install ESP32 firmware 
```
c:\>python esptool.py --chip esp32 --port COM5 write_flash -z 0x1000 esp32-idf3-20210202-v1.14.bin 
```

Black box wire connect

```
LED1 GPIO12
LED2 GPIO02  
```

RS485 - Modbus SDM120 baudrate->2400 

```
modbus = uModBusSerial(1, baudrate=2400, pins=(27, 26),ctrl_pin=25) #,ctrl_pin=25
RS485_DIR GPIO25
RS485_RX  GPIO26
RS485_TX  GPIO27
```
UART 
```
ESP32_RXD -> GPIO34
ESP32_TXD -> GPIO32 
```
SPI arduino IDE 

```
const lmic_pinmap lmic_pins = {
    .nss = 16, 
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 4,
    .dio = {/*dio0*/ 15, /*dio1*/ 13, /*dio2*/ LMIC_UNUSED_PIN}
};

//SPI.begin(SCK, MISO, MOSI, SS);
SPI.begin(18,19,23); 

SCK -> 18
MISO -> 19
MOSI -> 23
```

SPI uLora micropython -> Lolin32
```
LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)
```

SPI uLora micropython -> #Blackboard 
```
LORA_CS = const(16)  #18
LORA_SCK = const(18)  #5
LORA_MOSI = const(23)  #27 lolin32 connect
LORA_MISO = const(19)
LORA_IRQ = const(15)   #26
LORA_RST = const(4)   #14
```

softI2C
```
i2c = SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))  # heltec 5/4
```

I2C #Blackboard 
```
i2c = SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))  # heltec 5/4
```

![ScreenShot](https://github.com/worrajak/ESP32-micropython/blob/main/IMG_9148.jpg?raw=true)  

![ScreenShot](https://github.com/worrajak/ESP32-micropython/blob/main/IMG_9153.jpg?raw=true)  

![ScreenShot](https://github.com/worrajak/ESP32-micropython/blob/main/Circuit.jpg?raw=true)  
