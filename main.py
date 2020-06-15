import sys
from os import path
import pickle
from PySide2.QtWidgets import (
    QMainWindow,
    QApplication,
    QFileDialog,
    QAbstractItemView,
    QTableWidgetItem,
)
from PySide2.QtCore import QTimer, Slot

from ui.ui_mainwindow import Ui_MainWindow
from core.command import SCPI
from core.background import BackgroundThread
from core.xl import Xl

BASE_DIR = path.dirname(__file__)

PORT_NAME = path.join(BASE_DIR, "pkl/portName.pkl")
INPUT_FILE_PATH = path.join(BASE_DIR, "pkl/inputFilePath.pkl")
OUTPUT_DIR_PATH = path.join(BASE_DIR, "pkl/outputDirPath.pkl")


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

        if path.exists(PORT_NAME):
            with open(PORT_NAME, "rb") as f:
                self.port_name = pickle.load(f)
                self.comboBox.addItem(self.port_name)
        else:
            self.port_name = None

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

        self.inputTableWidget.setColumnCount(4)
        self.inputTableWidget.setHorizontalHeaderLabels(
            ["No.", "전압(V)", "전류(A)", "작동 시간(s)"]
        )
        self.inputTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["시간", "전압(V)", "전류(A)",]
        )
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnWidth(0, 300)

        self.background_thread.update_signal.connect(self.update_data)
        self.background_thread.save_signal.connect(self.save)
        self.background_thread.finish_signal.connect(self.finish)

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
                self.port_name = self.comboBox.currentText()
                self.controller.set_port(self.port_name)
                with open(PORT_NAME, "wb") as f:
                    pickle.dump(self.port_name, f)
            else:
                print("Set up RS-232 port.")
                return

            if self.inputFilePath is not None and path.exists(
                self.inputFilePath
            ):
                input_data = self.xl.load_input_data(self.inputFilePath)
                self.update_input_table(input_data)
            else:
                print("Set up input-file path.")
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
                input_data, operation_queue, repeat, interval
            )
            self.background_thread.start()

    def stop(self):
        self.background_thread.stop()
        QTimer.singleShot(1000, self._stop)

    def _stop(self):
        self.is_operating = False
        self.startButton.setEnabled(True)
        self.saveButton.setEnabled(True)

    def update_input_table(self, input_data):
        self.inputTableWidget.setRowCount(len(input_data))
        i = 0
        for key, item in input_data.items():
            print(item)
            self.inputTableWidget.setItem(i, 0, QTableWidgetItem(str(key)))
            self.inputTableWidget.setItem(i, 1, QTableWidgetItem(str(item[0])))
            self.inputTableWidget.setItem(i, 2, QTableWidgetItem(str(item[1])))
            self.inputTableWidget.setItem(i, 3, QTableWidgetItem(str(item[2])))
            i += 1

    @Slot(str)
    def save(self, date_str):
        if date_str:
            pass
        else:
            pass

    @Slot(None)
    def finish(self):
        self._stop()

    @Slot(list)
    def update_data(self, data):
        print(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
