# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 3)

        self.updatePortButton = QPushButton(self.centralwidget)
        self.updatePortButton.setObjectName(u"updatePortButton")

        self.gridLayout.addWidget(self.updatePortButton, 2, 4, 1, 2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.inputFile = QLineEdit(self.centralwidget)
        self.inputFile.setObjectName(u"inputFile")
        self.inputFile.setDragEnabled(True)
        self.inputFile.setReadOnly(True)

        self.gridLayout.addWidget(self.inputFile, 3, 1, 1, 3)

        self.findInputFileButton = QPushButton(self.centralwidget)
        self.findInputFileButton.setObjectName(u"findInputFileButton")

        self.gridLayout.addWidget(self.findInputFileButton, 3, 4, 1, 2)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.outputDir = QLineEdit(self.centralwidget)
        self.outputDir.setObjectName(u"outputDir")
        self.outputDir.setDragEnabled(True)
        self.outputDir.setReadOnly(True)

        self.gridLayout.addWidget(self.outputDir, 4, 1, 1, 3)

        self.findOutputDirButton = QPushButton(self.centralwidget)
        self.findOutputDirButton.setObjectName(u"findOutputDirButton")

        self.gridLayout.addWidget(self.findOutputDirButton, 4, 4, 1, 2)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.operationRange = QLineEdit(self.centralwidget)
        self.operationRange.setObjectName(u"operationRange")

        self.gridLayout.addWidget(self.operationRange, 5, 1, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 2, 1, 1)

        self.repeatSpinBox = QSpinBox(self.centralwidget)
        self.repeatSpinBox.setObjectName(u"repeatSpinBox")
        self.repeatSpinBox.setMinimum(1)
        self.repeatSpinBox.setMaximum(999)

        self.gridLayout.addWidget(self.repeatSpinBox, 5, 3, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 4, 1, 1)

        self.intervalSpinBox = QSpinBox(self.centralwidget)
        self.intervalSpinBox.setObjectName(u"intervalSpinBox")
        self.intervalSpinBox.setMinimum(2)
        self.intervalSpinBox.setMaximum(999)

        self.gridLayout.addWidget(self.intervalSpinBox, 5, 5, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startButton = QPushButton(self.frame)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout.addWidget(self.startButton)

        self.stopButton = QPushButton(self.frame)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout.addWidget(self.stopButton)

        self.saveButton = QPushButton(self.frame)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)


        self.gridLayout.addWidget(self.frame, 6, 0, 1, 6)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 7, 0, 1, 6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"XG-850 controller", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ud3ec\ud2b8", None))
        self.updatePortButton.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815 \ud30c\uc77c", None))
        self.findInputFileButton.setText(QCoreApplication.translate("MainWindow", u"Find", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5 \ud3f4\ub354", None))
        self.findOutputDirButton.setText(QCoreApplication.translate("MainWindow", u"Find", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\uc218\ud589 \ubc94\uc704", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\ubc18\ubcf5 \ud69f\uc218", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\ub370\uc774\ud130 \uc218\uc9d1 \uac04\uaca9(s)", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

