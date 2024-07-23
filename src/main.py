# -*- coding: utf-8 -*-
# src/main.py

"""This module provides the RP Contacts application"""

import sys

from PyQt6.QtWidgets import QApplication as qapp

from .views import Window

def main():
    """RP Contacts main function"""
    app = qapp(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
