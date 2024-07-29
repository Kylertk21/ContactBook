# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt6.QtWidgets import (
    QAbstractItemView as absview,
    QHBoxLayout as qbox,
    QMainWindow as win,
    QPushButton as pushbtn,
    QTableView as tview,
    QVBoxLayout as vbox,
    QWidget as widg,
    QDialog,
    QDialogButtonBox as bbox,
    QFormLayout as flayout,
    QLineEdit as ledit,
    QMessageBox as msbox
)
from PyQt6.QtCore import Qt
from .model import ContactsModel
from .database import createConnection

class Window(win):
    """Main Window"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("Rp Contacts")
        self.resize(550,250)
        self.centralWidget = widg()
        self.setCentralWidget(self.centralWidget)
        self.layout = qbox()
        self.centralWidget.setLayout(self.layout)
        
        if not createConnection("contacts"):
            msbox.critical(None, 'Database Connection', 'Database connection failed!')
            exit(1)
        
        self.contactsModel = ContactsModel()
        self.setupUI()
    
    def setupUI(self):
        """Setup Main Window GUI"""
        self.table = tview()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(absview.SelectionBehavior.SelectRows)
        
        self.addBtn = pushbtn("Add...")
        self.addBtn.clicked.connect(self.openAddDialog)
        self.delBtn = pushbtn("Delete")
        self.clrAll = pushbtn("Clear All")

        layout = vbox()
        layout.addWidget(self.addBtn)
        layout.addWidget(self.delBtn)
        layout.addStretch()
        layout.addWidget(self.clrAll)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

        self.table
    
    def openAddDialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

class AddDialog(QDialog):
    """Add Contact Dialog Box"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = vbox()
        self.setLayout(self.layout)
        self.data = None
        
        self.setupUI()
    
    def setupUI(self):
        """Setup Add Contact Dialog's GUI"""
        self.nameField = ledit()
        self.nameField.setObjectName("Name")
        self.phoneField = ledit()
        self.phoneField.setObjectName("Phone")
        self.emailField = ledit()
        self.emailField.setObjectName("Email")

        layout = flayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Phone:", self.phoneField)
        layout.addRow("Email:", self.emailField)
        self.layout.addLayout(layout)

        self.buttonsBox = bbox(self)
        self.buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonsBox.setStandardButtons(
            bbox.StandardButton.Ok | bbox.StandardButton.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        # TODO: add more robust validations rules
        """Accept data from dialog box"""
        self.data = []
        for field in (self.nameField, self.phoneField, self.emailField):
            if not field.text():
                msbox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None
                return
            self.data.append(field.text())

        super().accept()


