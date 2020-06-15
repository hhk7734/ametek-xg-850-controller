from datetime import datetime
from PySide2.QtCore import QThread, Signal
import time


def millis():
    return int(round(time.time() * 1000))


class BackgroundThread(QThread):
    update_signal = Signal(list)
    finish_signal = Signal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.is_running = False

    def set_data(self, input_data, operation_queue, repeat, interval):
        self.input_data = input_data
        self.operation_queue = operation_queue
        self.repeat = repeat
        self.interval = interval

    def run(self):
        self.is_running = True
        sec = 0
        count = 0
        max_count = len(self.operation_queue)

        self.controller.connect()
        self.controller.set_address(1)

        while self.is_running:
            current_millis = millis()
            index = self.operation_queue[count]

            if sec == self.input_data[index][2]:
                """
                setup
                """
                self.update_data()
                self.msleep(20)

                count += 1
                if max_count == count:
                    self.repeat -= 1
                    if self.repeat == 0:
                        self.finish_signal.emit(
                            datetime.now.strftime("%Y-%d-%m-%H-%M-%S")
                        )
                        break
                    count = 0

                index = self.operation_queue[count]

                self.controller.set_init()
                self.msleep(50)

                self.controller.set_voltage(self.input_data[index][0])
                self.msleep(20)
                self.controller.set_current(self.input_data[index][1])

                sec = 0
                continue

            if sec % self.interval == 0:
                """
                update current status
                """
                self.update_data()

            delta = millis() - current_millis
            if 1000 - delta > 0:
                self.msleep(1000 - delta)
            sec += 1

        self.controller.disconnect()

    def stop(self):
        self.is_running = False

    def update_data(self):
        data = [
            datetime.now(),
            self.controller.get_voltage(),
            self.controller.get_current(),
        ]
        self.update_signal.emit(data)
