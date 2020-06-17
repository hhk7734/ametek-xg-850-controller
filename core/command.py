import os
import serial
import time

if os.name == "nt":
    from serial.tools.list_ports_windows import comports
elif os.name == "posix":
    from serial.tools.list_ports_posix import comports


class SCPI:
    def __init__(self):
        self.uart = serial.Serial(baudrate=57600, timeout=0)
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

    def read_until(self):
        time.sleep(0.03)
        string = b""
        start_time = time.time()
        while time.time() - start_time < 5:
            data = self.uart.read(1)
            if data != b"":
                if data != b"\r":
                    string += data
                else:
                    return string
        return None

    def set_address(self, address):
        self.uart.write("*ADR {}\r".format(address).encode())

    def set_output(self, output):
        if output:
            self.uart.write(b":OUTP ON\r")
        else:
            self.uart.write(b":OUTP OFF\r")

    def get_voltage(self):
        self.uart.write(b"MEAS:VOLT?\r")
        return float(self.read_until())

    def set_voltage(self, voltage):
        self.uart.write("SOUR:VOLT {}\r".format(voltage).encode())

    def set_voltage_protection(self, voltage):
        self.uart.write("SOUR:VOLT:PROT {}\r".format(voltage).encode())

    def get_current(self):
        self.uart.write(b"MEAS:CURR?\r")
        return float(self.read_until())

    def set_current(self, current):
        self.uart.write("SOUR:CURR {}\r".format(current).encode())

    def set_current_protection(self, current):
        self.uart.write("SOUR:CURR:PROT {}\r".format(current).encode())
