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
        self.layout = qbox()
        self.centralWidget.setLayout(self.layout)
        
        if not createConnection("contacts"):
            msbox.critical(None, 'Database Connection', 'Database connection failed!')
            exit(1)
        
        self.contactsModel = ContactsModel()
        self.stackedWidget = stack()
        self.layout.addWidget(self.stackedWidget)

        self.setupUI()
    
    def setupUI(self):
        """Setup Main Window GUI"""
        self.table = tview()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(absview.SelectionBehavior.SelectRows)
        
        self.addBtn = pushbtn("Add...")
        self.addBtn.clicked.connect(self.openAddDialog)
        self.delBtn = pushbtn("Delete")
        self.delBtn.clicked.connect(self.deleteContact)
        
        #TODO: Add functions for Next and Previous buttons
        self.nextBtn = pushbtn("Next")
        self.nextBtn.clicked.connect(self.nextContact)
        self.prevBtn = pushbtn("Previous")
        self.prevBtn.clicked.connect(self.prevContact)

        self.clrAll = pushbtn("Clear All")
        self.clrAll.clicked.connect(self.clearContacts)

        navLayout = qbox()
        navLayout.addWidget(self.prevBtn)
        navLayout.addWidget(self.nextBtn)
        
        ctlLayout = qbox()
        ctlLayout.addWidget(self.addBtn)
        ctlLayout.addWidget(self.delBtn)
        ctlLayout.addWidget(self.clrAll)

        self.layout.addLayout(navLayout)
        self.layout.addWidget(self.stackedWidget)
        self.layout.addLayout(ctlLayout)

        self.updatePages()
    
    def updatePages(self):
        """Updates pages in the stacked widget"""
        while self.stackedWidget.count():
            widget = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()

        contacts = self.contactsModel.fetchContacts()

        for contact in contacts:
            page = widg()
            layout = vbox(page)

            contactBox = gbox("Contacts")
            contactLayout = flayout(contactBox)
            contactLayout.addRow("Name:", label(contact['name']))
            contactLayout.addRow("Phone:", label(contact['phone']))
            contactLayout.addRow("Email:", label(contact['email']))

            layout.addWidget(contactBox)
            self.stackedWidget.addWidget(page)

    def openAddDialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.updatePages()
            self.table.setModel(self.contactsModel.model)
            self.table.resizeColumnsToContents()

    def deleteContact(self):
        """Deletes Contact From DB (GUI)"""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        messageBox = msbox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            msbox.StandardButton.Ok | msbox.StandardButton.Cancel
        )

        if messageBox == msbox.StandardButton.Ok:
            self.contactsModel.deleteContact(row)
            self.updatePages()

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


