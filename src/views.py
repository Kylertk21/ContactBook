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
)
from .model import ContactsModel

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
        self.contactsModel = ContactsModel()
        self.setupUI()
    
    def setupUI(self):
        """Setup Main Window GUI"""
        self.table = tview()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(absview.SelectionBehavior.SelectRows)
        
        self.addBtn = pushbtn("Add...")
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


