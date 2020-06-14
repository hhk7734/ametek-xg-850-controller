import serial
import time

from serial.tools.list_ports_windows import comports


class SCPI:
    def __init__(self):
        self.uart = serial.Serial(baudrate=9600, timeout=0)
        self.ports = {}

    def get_port(self):
        self.ports.clear()
        for port, desc, _ in comports():
            self.ports[port] = desc

    def set_port(self, port):
        self.disconnect()
        self.uart.port = port

    def set_baudrate(self, baudrate):
        self.uart.baudrate = baudrate

    def connect(self):
        self.uart.open()

    def disconnect(self):
        self.uart.close()

    def set_address(self, address):
        self.uart.write("*ADR {}\r".format(address).encode())

    def set_voltage(self, voltage):
        pass

    def set_voltage_protection(self, voltage):
        pass

    def set_current(self, current):
        pass

    def set_current_protection(self, current):
        pass
