from datetime import datetime
import logging
from PySide2.QtCore import QThread, Signal
import time


log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def millis():
    return int(round(time.time() * 1000))


class BackgroundThread(QThread):
    update_signal = Signal(list)
    save_signal = Signal(str)
    finish_signal = Signal()

    _MSLEEP_MS = 30

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
        self.msleep(self._MSLEEP_MS)

        """
        First operation configuration
        """
        index = self.operation_queue[count]
        self.controller.set_voltage(self.input_data[index][0])
        self.msleep(self._MSLEEP_MS)
        self.controller.set_current(self.input_data[index][1])
        self.msleep(self._MSLEEP_MS)
        self.controller.set_output(True)
        self.msleep(self._MSLEEP_MS)

        while self.is_running:
            current_millis = millis()
            index = self.operation_queue[count]

            if sec == self.input_data[index][2]:
                """
                When an operation is finished, it read current device setup.
                """
                self.update_data()
                self.msleep(self._MSLEEP_MS)

                count += 1
                if max_count == count:
                    self.repeat -= 1
                    if self.repeat == 0:
                        break
                    count = 0

                """
                Next Operation
                """
                index = self.operation_queue[count]

                self.controller.set_voltage(self.input_data[index][0])
                self.msleep(self._MSLEEP_MS)
                self.controller.set_current(self.input_data[index][1])
                self.msleep(self._MSLEEP_MS)

                sec = 0
                continue

            if sec % self.interval == 0:
                """
                Update current status
                """
                self.update_data()

            delta = millis() - current_millis
            log.info("BackgroundThread: run: delta: {}".format(delta))
            if 1000 - delta > 0:
                self.msleep(1000 - delta)
            sec += 1

        self.save_signal.emit(datetime.now().strftime("%Y-%d-%m-%H-%M-%S"))
        self.finish_signal.emit()

        self.controller.set_output(False)
        self.controller.disconnect()
        log.debug("finish")

    def stop(self):
        self.is_running = False

    def update_data(self):
        try:
            data = [
                datetime.now(),
                self.controller.get_voltage(),
                self.controller.get_current(),
            ]
            self.update_signal.emit(data)
        except Exception as e:
            log.error(e)
            self.stop()
