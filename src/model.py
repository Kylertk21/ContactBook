# -*- coding: utf-8 -*-
# src/model.py

"""Provides a model to manage the contacts table"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel as qtmodel

class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        tableModel = qtmodel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(qtmodel.EditStrategy.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Name", "Phone", "Email")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel
