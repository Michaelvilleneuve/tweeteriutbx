from I2C import ARDUINO_ADDRESS, NEW_RASPBERRY
import smbus
import time

class I2C:
    def __init__(self):
        self.arduino_address = ARDUINO_ADDRESS
        self._arduino = smbus.SMBus(NEW_RASPBERRY)
