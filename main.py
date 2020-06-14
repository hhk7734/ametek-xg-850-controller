import sys
from os import path
import pickle
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog

from ui.ui_mainwindow import Ui_MainWindow
from core.command import SCPI


class Main_window(QMainWindow, Ui_MainWindow):
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

        if path.exists("pkl/inputFilePath.pkl"):
            with open("pkl/inputFilePath.pkl", "rb") as f:
                self.inputFilePath = pickle.load(f)
                self.inputFile.setText(self.inputFilePath)
        else:
            self.inputFilePath = None

        if path.exists("pkl/outputDirPath.pkl"):
            with open("pkl/outputDirPath.pkl", "rb") as f:
                self.outputDirPath = pickle.load(f)
                self.outputDir.setText(self.outputDirPath)
        else:
            self.outputDirPath = None

        self.updatePortButton.clicked.connect(self.update_ports)
        self.findInputFileButton.clicked.connect(self.find_input_file)
        self.findOutputDirButton.clicked.connect(self.find_output_dir)

    def update_ports(self):
        self.comboBox.clear()
        self.controller.get_port()
        for key, value in self.controller.ports.items():
            self.comboBox.addItem(key + " -> " + value)

    def find_input_file(self):
        new_input_file = QFileDialog.getOpenFileName(
            self, "Select File", self.inputFilePath, "Excel (*xlsx)"
        )
        if new_input_file[0] != "":
            self.inputFilePath = new_input_file[0]
            self.inputFile.setText(self.inputFilePath)
            with open("pkl/inputFilePath.pkl", "wb") as f:
                pickle.dump(self.inputFilePath, f)

    def find_output_dir(self):
        new_output_dir = QFileDialog.getExistingDirectory(
            self, "Select Folder", self.outputDirPath
        )
        if new_output_dir:
            self.outputDirPath = new_output_dir
            self.outputDir.setText(self.outputDirPath)
            with open("pkl/outputDirPath.pkl", "wb") as f:
                pickle.dump(self.outputDirPath, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
