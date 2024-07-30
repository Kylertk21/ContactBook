# -*- coding: utf-8 -*-
# src/model.py

"""Provides a model to manage the contacts table"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel as qtmodel
from PyQt6.QtWidgets import QMessageBox as msbox

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
    
    def addContact(self,data):
        """Add a contact to the database"""
        rows = self.model.rowCount()
        self.model.insertRows(rows,1)
        self.model.setData(self.model.index(rows, 1), data[0])
        self.model.setData(self.model.index(rows, 2), data[1])
        self.model.setData(self.model.index(rows, 3), data[2])
        if not self.model.submitAll():
            msbox.critical(None, "Database Error", 
                           f"Error submitting data: {self.model.lastError().text()}")
        self.model.select()

    def deleteContact(self, row):
        """Removes Contacts From DB"""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clearContacts(self):
        """Clears all contacts in the DB"""
        self.model.setEditStrategy(qtmodel.EditStrategy.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(qtmodel.EditStrategy.OnFieldChange)
        self.model.select()

    def fetchContacts(self):
        """Fetch all contacts from DB"""
        contacts = []
        self.model.select()
        for row in range(self.model.rowCount()):
            contact = {
                'name': self.model.data(self.model.index(row, 1)),
                'phone': self.model.data(self.model.index(row, 2)),
                'email': self.model.data(self.model.index(row, 3))
            }
            contacts.append(contact)
        return contacts