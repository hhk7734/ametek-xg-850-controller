from datetime import datetime
import sys
from os import path
import pickle
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide2.QtCore import QThread, Slot, Signal, QTimer
import time

from ui.ui_mainwindow import Ui_MainWindow
from core.command import SCPI
from core.xl import Xl

INPUT_FILE_PATH = path.join(path.dirname(__file__), "pkl/inputFilePath.pkl")
OUTPUT_DIR_PATH = path.join(path.dirname(__file__), "pkl/outputDirPath.pkl")


def millis():
    return int(round(time.time() * 1000))


class BackgroundThread(QThread):
    read_status = Signal(list)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.is_running = False

    def set_data(self, setup_data, operation_queue, repeat, interval):
        self.setup_data = setup_data
        self.operation_queue = operation_queue
        self.repeat = repeat
        self.interval = interval

    def run(self):
        self.is_running = True
        count = 0
        while self.is_running:
            current_millis = millis()

            if count > 0:
                if count % self.interval == 0:
                    pass


            delta = millis() - current_millis
            if 1000 - delta > 0:
                self.msleep(1000 - delta)

    def stop(self):
        self.is_running = False


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Ui 클래스 상속
    """

    def __init__(self):
        super().__init__()
        """
        Ui 설정
        """
        self.setupUi(self)

        self.controller = SCPI()
        self.xl = Xl()
        self.background_thread = BackgroundThread(self.controller)

        self.is_operating = False

        if path.exists(INPUT_FILE_PATH):
            with open(INPUT_FILE_PATH, "rb") as f:
                self.inputFilePath = pickle.load(f)
                self.inputFile.setText(self.inputFilePath)
        else:
            self.inputFilePath = None

        if path.exists(OUTPUT_DIR_PATH):
            with open(OUTPUT_DIR_PATH, "rb") as f:
                self.outputDirPath = pickle.load(f)
                self.outputDir.setText(self.outputDirPath)
        else:
            self.outputDirPath = None

        self.updatePortButton.clicked.connect(self.update_ports)
        self.findInputFileButton.clicked.connect(self.find_input_file)
        self.findOutputDirButton.clicked.connect(self.find_output_dir)

        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.saveButton.clicked.connect(self.save)

    def update_ports(self):
        self.comboBox.clear()
        self.controller.get_port()
        for key, value in self.controller.ports.items():
            self.comboBox.addItem(key, userData=value)

    def find_input_file(self):
        new_input_file = QFileDialog.getOpenFileName(
            self, "Select File", self.inputFilePath, "Excel (*xlsx)"
        )
        if new_input_file[0] != "":
            self.inputFilePath = new_input_file[0]
            self.inputFile.setText(self.inputFilePath)
            with open(INPUT_FILE_PATH, "wb") as f:
                pickle.dump(self.inputFilePath, f)

    def find_output_dir(self):
        new_output_dir = QFileDialog.getExistingDirectory(
            self, "Select Folder", self.outputDirPath
        )
        if new_output_dir:
            self.outputDirPath = new_output_dir
            self.outputDir.setText(self.outputDirPath)
            with open(OUTPUT_DIR_PATH, "wb") as f:
                pickle.dump(self.outputDirPath, f)

    def start(self):
        if not self.is_operating:
            if self.comboBox.currentText():
                self.controller.set_port = self.comboBox.currentText()
            else:
                print("Set up RS-232 port.")
                return

            if self.inputFilePath is not None:
                setup_data = self.xl.load_setup_data(self.inputFilePath)
            else:
                print("Set up setup file path.")
                return

            if self.operationRange.text():
                operation_range = self.operationRange.text().strip()
                operation_range = operation_range.split(",")
                operation_queue = []
                for operation in operation_range:
                    if operation.find("-") != -1:
                        index = operation.find("-")
                        start_num = int(operation[:index])
                        end_num = int(operation[index + 1 :])
                        for i in range(start_num, end_num + 1):
                            operation_queue.append(i)
                    else:
                        operation_queue.append(int(operation))
            else:
                print("Set up operation range.")
                return

            self.is_operating = True
            self.startButton.setEnabled(False)
            self.saveButton.setEnabled(False)

            repeat = self.repeatSpinBox.value()
            interval = self.intervalSpinBox.value()

            self.background_thread.set_data(
                setup_data, operation_queue, repeat, interval
            )
            self.background_thread.start()

    def stop(self):
        self.background_thread.stop()
        QTimer.singleShot(1000, self._stop)

    def _stop(self):
        self.is_operating = False
        self.startButton.setEnabled(True)
        self.saveButton.setEnabled(True)

    def save(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
