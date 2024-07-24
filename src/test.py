from database import createConnection
from PyQt6.QtWidgets import QApplication as qapp
import sys

app = qapp(sys.argv)

createConnection("contacts")

from PyQt6.QtSql import QSqlDatabase
db = QSqlDatabase.database()
db.tables()

from PyQt6.QtSql import QSqlQuery as query

insert = query()
insert.prepare(
    """
    INSERT INTO contacts (
    name,
    phone,
    email
    )
    VALUES (?,?,?)
    """
)

printout = query()
printout.prepare(
    """
    SELECT * FROM contacts
    """
)

clear = query()
clear.prepare(
    """
    DELETE FROM contacts
    """
)

data = [
    ("Linda", "1970000987", "linda@example.com"),
    ("Joe", "1111111111", "joe@example.com"),
    ("Lara", "1234567890", "lara@example.com"),
    ("David", "2468024681", "david@example.com"),
    ("Jane", "8888888888", "jane@example.com"),
]

for name, phone, email in data:
    insert.addBindValue(name)
    insert.addBindValue(phone)
    insert.addBindValue(email)
    insert.exec()


printout.exec()

while printout.next():
    id = printout.value(0)
    name = printout.value(1)
    phone = printout.value(2)
    email = printout.value(3)
    print(f"ID: {id}, Name: {name}, Phone: {phone}, Email: {email}")

clear.exec()