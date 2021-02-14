# Somsak Limawaongpranee 
# Modbus lib https://github.com/techbase123/micropython-modbus
from uModBusSerial import uModBusSerial
from struct import *
modbus = uModBusSerial(1, baudrate=2400, pins=(27, 26),ctrl_pin=25) #,ctrl_pin=25

def IEEE(Lowbit, highbit):
    mypack = pack('>HH', Lowbit, highbit)
    f = unpack('>f', mypack)
    rstr = f[0]
    return (rstr)

slave_addr = 0x01
starting_address = 0x00
register_quantity = 88
signed = True
register_value = modbus.read_input_registers(slave_addr, starting_address, register_quantity, signed)
Volt = IEEE(register_value[0], register_value[1])
Amp = IEEE(register_value[6], register_value[7])
PowerF = IEEE(register_value[30], register_value[31])
Freq = IEEE(register_value[70], register_value[71])
ImportPower = IEEE(register_value[72], register_value[73])

print("Import Power:", ImportPower, "kWh")
print("        Volt:", Volt)
print("     Current:", Amp, "Amp")
print("Power Factor:", PowerF)
print("        Freq:", Freq, "Hz")

