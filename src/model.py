# -*- coding: utf-8 -*-
# src/model.py

"""Provides a model to manage the contacts table"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel as qtmodel, QSqlQuery
from PyQt6.QtWidgets import QMessageBox as msbox, QStackedWidget as qstack

class ContactsModel:
    def __init__(self):
        self.model = self._createModel()
        self.contacts = self.fetchContacts()

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

    def deleteContact(self, index):
        """Removes Contacts From DB"""
        if index >= 0:
            self.model.removeRows(index, 1)
            if not self.model.submitAll():
                msbox.critical(None, "Error deleting from DB: {self.model.lastError().text()}")
                return False
            return True
        return False

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
                'id': self.model.data(self.model.index(row, 0)),
                'name': self.model.data(self.model.index(row, 1)),
                'phone': self.model.data(self.model.index(row, 2)),
                'email': self.model.data(self.model.index(row, 3))
            }
            contacts.append(contact)
        return contacts
    
    def updateContacts(self, contact_id, contact):
        """Saves field edits to DB"""

        query = QSqlQuery()
        query.prepare("""
                      UPDATE contacts
                      SET name = :name, phone = :phone, email = :email
                      WHERE id = :id
                      """)
        query.bindValue(":name", contact['name'])
        query.bindValue(":phone", contact['phone'])
        query.bindValue(":email", contact['email'])
        query.bindValue(":id", contact_id)

        return query.exec()