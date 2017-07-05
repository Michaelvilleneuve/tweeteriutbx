import smbus
import time


class Arduino:
    def __init__(self):
        self.address = 0x12
        self._arduino = smbus.SMBus(1)

    def get_arduino(self):
        return self._arduino

    def send_followers_count(self, param):
        msg = self.string_to_bytes(param)
        self._arduino.write_i2c_block_data(self.address, 0, msg)
        time.sleep(0.5)
        res = self._arduino.read_byte(self.address)
        return res

    @staticmethod
    def string_to_bytes(param):
        ret_val = []
        for c in param:
            ret_val.append(ord(c))
        return ret_val
