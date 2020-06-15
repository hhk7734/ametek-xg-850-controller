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

    def set_init(self):
        self.uart.write(b":INIT\r")
        # self.uart.writE(b"SYST:RES\r")

    def set_output(self, output):
        if output:
            self.uart.write(b":OUTP ON\r")
        else:
            self.uart.write(b":OUTP OFF\r")

    def get_voltage(self):
        self.uart.write(b"MEAS:VOLT?\r")
        return self.uart.read_until("\r").decode()

    def set_voltage(self, voltage):
        self.uart.write("SOUR:VOLT {}\r".format(voltage).encode())

    def set_voltage_protection(self, voltage):
        self.uart.write("SOUR:VOLT:PROT {}\r".format(voltage).encode())

    def get_current(self):
        self.uart.write(b"MEAS:CURR?\r")
        return self.uart.read_until("\r").decode()

    def set_current(self, current):
        self.uart.write("SOUR:CURR {}\r".format(current).encode())

    def set_current_protection(self, current):
        self.uart.write("SOUR:CURR:PROT {}\r".format(current).encode())
