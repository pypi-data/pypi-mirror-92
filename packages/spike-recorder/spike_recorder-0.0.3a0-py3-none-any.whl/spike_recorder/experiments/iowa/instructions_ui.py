# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\spike_recorder\experiments\iowa\instructions.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_instructions(object):
    def setupUi(self, dialog_instructions):
        dialog_instructions.setObjectName("dialog_instructions")
        dialog_instructions.resize(540, 258)
        dialog_instructions.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog_instructions)
        self.buttonBox.setGeometry(QtCore.QRect(170, 220, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(dialog_instructions)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 471, 101))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog_instructions)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 130, 491, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textbox_file = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.textbox_file.setObjectName("textbox_file")
        self.horizontalLayout.addWidget(self.textbox_file)
        self.button_browse = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.button_browse.setObjectName("button_browse")
        self.horizontalLayout.addWidget(self.button_browse)

        self.retranslateUi(dialog_instructions)
        self.buttonBox.accepted.connect(dialog_instructions.accept)
        self.buttonBox.rejected.connect(dialog_instructions.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog_instructions)

    def retranslateUi(self, dialog_instructions):
        _translate = QtCore.QCoreApplication.translate
        dialog_instructions.setWindowTitle(_translate("dialog_instructions", "Instructions"))
        self.label_2.setText(_translate("dialog_instructions", "Subject will make 100 draws from various decks, trying to ascertain the underlying rules and maximize profit. Subjects will report when they have a hunch about deck rules and when they’re “pretty sure” of deck rules.\n"
""))
        self.label.setText(_translate("dialog_instructions", "Output File:"))
        self.button_browse.setText(_translate("dialog_instructions", "..."))

