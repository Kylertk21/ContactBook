# -*- coding: utf-8 -*-
# src/main.py

"""This module provides the RP Contacts application"""

import sys

from PyQt6.QtWidgets import QApplication as qapp
from .database import createConnection 
from .views import Window

def main():
    """RP Contacts main function"""
    app = qapp(sys.argv)

    with open("src/stylesheet.css", "r") as file:
        app.setStyleSheet(file.read())

    if not createConnection("contacts"):
        sys.exit(1)

    win = Window()
    win.show()
    sys.exit(app.exec())
