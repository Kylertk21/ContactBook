# -*- coding: utf-8 -*-
# src/database.py

"""Provides Database Connection"""

from PyQt6.QtWidgets import QMessageBox as msbox
from PyQt6.QtSql import QSqlDatabase as db, QSqlQuery as query
from PyQt6.QtWidgets import QApplication as qapp

def _createContactsTable():
    """Creates contacts table in db"""
    createTableQuery = query()
    createtable = createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            phone VARCHAR(10),
            email VARCHAR(40) NOT NULL)
        """
    )
    if not createtable:
        print("Failed to create table:", createTableQuery.lastError().text())
    return createtable

def createConnection(databaseName):
    """Creates and opens a database connection"""

    connection = db.addDatabase("QPSQL")
    connection.setDatabaseName(databaseName)
    connection.setHostName("localhost")
    connection.setUserName("kyler")
    connection.setPassword("icedog")
    
    if not connection.open():
        msbox.warning(
            None,
            "RP Contact",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    
    _createContactsTable()
    return True