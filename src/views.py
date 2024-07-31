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
    QMessageBox as msbox,
    QStackedWidget as stack,
    QLabel as label,
    QGroupBox as gbox
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
        self.mainLayout = vbox()
        self.centralWidget.setLayout(self.mainLayout)
        
        if not createConnection("contacts"):
            msbox.critical(None, 'Database Connection', 'Database connection failed!')
            exit(1)
        
        self.contactsModel = ContactsModel()
        self.stackedWidget = stack()
        self.mainLayout.addWidget(self.stackedWidget)

        self.setupUI()
    
    def setupUI(self):
        """Setup Main Window GUI"""

        self.addBtn = pushbtn("Add...")
        self.addBtn.clicked.connect(self.openAddDialog)
        self.clrAll = pushbtn("Clear All")
        self.clrAll.clicked.connect(self.clearContacts)

        topLayout = qbox()
        topLayout.addStretch()
        topLayout.addWidget(self.addBtn)
        topLayout.addWidget(self.clrAll)
        self.mainLayout.addLayout(topLayout)

        self.mainLayout.addWidget(self.stackedWidget)

        self.nextBtn = pushbtn("Next")
        self.nextBtn.clicked.connect(self.nextContact)
        self.prevBtn = pushbtn("Previous")
        self.prevBtn.clicked.connect(self.prevContact)

        navLayout = qbox()
        navLayout.addWidget(self.prevBtn)
        navLayout.addWidget(self.nextBtn)

        self.mainLayout.addLayout(navLayout)
     
        self.updatePages()
    
    def updatePages(self):
        """Updates pages in the stacked widget"""
        while self.stackedWidget.count():
            widget = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()

        contacts = self.contactsModel.fetchContacts()

        for index, contact in enumerate(contacts):
            page = widg()
            layout = vbox(page)

            contactBox = gbox("Contacts")
            contactLayout = flayout(contactBox)

            self.nameField = ledit()
            self.nameField.setText(contact['name'])
            self.nameField.setObjectName(f"Name_{index}")
            contactLayout.addRow("Name:", self.nameField)

            self.phoneField = ledit()
            self.phoneField.setText(contact['phone'])
            self.phoneField.setObjectName(f"Phone_{index}")
            contactLayout.addRow("Phone:", self.phoneField)

            self.emailField = ledit()
            self.emailField.setText(contact['email'])
            self.emailField.setObjectName(f"Email_{index}")
            contactLayout.addRow("Email:", self.emailField)

            delBtn = pushbtn("Delete")
            delBtn.clicked.connect(lambda _, i=index: self.deleteContact(i))
            contactLayout.addWidget(delBtn)

            saveBtn = pushbtn("Save")
            saveBtn.clicked.connect(lambda _, i=index: self.saveContact(i))
            contactLayout.addWidget(saveBtn)

            layout.addWidget(contactBox)
            self.stackedWidget.addWidget(page)

    def openAddDialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.updatePages()

    def deleteContact(self, index=None):
        """Deletes Contact From DB (GUI)"""
        if index is None:
            index = self.stackedWidget.currentIndex()

        if index < 0 or index >= self.stackedWidget.count():
            return
        
        messageBox = msbox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            msbox.StandardButton.Ok  |  msbox.StandardButton.Cancel
        )

        if messageBox == msbox.StandardButton.Ok:
            if self.contactsModel.deleteContact(index):
                msbox.information(self, 
                                  "Success",
                                  "Contact Deleted",
                                  msbox.StandardButton.Ok)
                self.updatePages()
            else:
                msbox.critical(self, 
                               "Failed to delete contact:",
                                "{self.model.lastError().text()}", 
                                msbox.StandardButton.Ok)
    def saveContact(self, index):
        """Saves Contact to DB (GUI)"""
        currentPage = self.stackedWidget.widget(index)
        nameField = currentPage.findChild(ledit, f"Name_{index}")
        phoneField = currentPage.findChild(ledit, f"Phone_{index}")
        emailField = currentPage.findChild(ledit, f"Email_{index}")
        
        contact = {
            'name': self.nameField.text(),
            'phone': self.phoneField.text(),
            'email': self.emailField.text()
        }

        contacts = self.contactsModel.fetchContacts()
        contact_id = contacts[index]['id']

        messageBox = msbox.warning(
            self,
            "Warning!",
            "Do you want to change the contact's data?",
            msbox.StandardButton.Ok  |  msbox.StandardButton.Cancel
        )

        if messageBox == msbox.StandardButton.Ok:
            if self.contactsModel.updateContacts(contact_id, contact):
                msbox.information(
                    self,
                    "Success",
                    "Contact updated successfully",
                    msbox.StandardButton.Ok
                )
                self.updatePages()
            else:
                msbox.critical(
                    self,
                    "Error",
                    "Failed to update contact: {self.model.lastError.text()}",
                    msbox.StandardButton.Ok
                )

    def nextContact(self):
        """Navigates to next contact page"""
        currentIndex = self.stackedWidget.currentIndex()
        if currentIndex < self.stackedWidget.count() - 1:
            self.stackedWidget.setCurrentIndex(currentIndex + 1)

    def prevContact(self):
        """Navigates to previous contact page"""
        currentIndex = self.stackedWidget.currentIndex()
        if currentIndex > 0:
            self.stackedWidget.setCurrentIndex(currentIndex - 1)


    def clearContacts(self):
        """Clears contacts from DB (GUI)"""
        messageBox = msbox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contacts?",
            msbox.StandardButton.Ok  |  msbox.StandardButton.Cancel
        )

        if messageBox == msbox.StandardButton.Ok:
            self.contactsModel.clearContacts()
            self.updatePages()

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


