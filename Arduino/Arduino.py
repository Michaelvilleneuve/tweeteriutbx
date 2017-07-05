import smbus
import time


class Arduino:
    def __init__(self):
        self.address = 0x12
        self._arduino = smbus.SMBus(1)

    def get_arduino(self):
        return self._arduino

    def send_followers_count(self, param):
        self._arduino.write_byte(self.address, param)
        time.sleep(0.5)
        res = self._arduino.read_byte(self.address)
        return res
