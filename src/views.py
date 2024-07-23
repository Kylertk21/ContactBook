# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt6.QtWidgets import (
    QHBoxLayout as qbl,
    QMainWindow as win,
    QWidget as widg,
)

class Window(win):
    """Main Window"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("Rp Contacts")
        self.resize(550,250)
        self.centralWidget = widg()
        self.setCentralWidget(self.centralWidget)
        self.layout = qbl()
        self.centralWidget.setLayout(self.layout)

