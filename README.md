# ESP32-micropython

install anaconda python -> download from website 

change firmware -> esp32-idf3-20210202-v1.14.bin to newest file 

change com port -> 

install ESP32 firmware 

c:\>python esptool.py --chip esp32 --port COM5 write_flash -z 0x1000 esp32-idf3-20210202-v1.14.bin 



Black box wire connect

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

SPI uLora micropython -> 
```
LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)
```

softI2C
```
i2c = SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))  # heltec 5/4
```
