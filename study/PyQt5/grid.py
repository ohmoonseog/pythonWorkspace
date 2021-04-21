from os.path import exists
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *


import sys

if not exists("tools.db"):
    print("File projects.db does not exist. Please run initdb.py.")
    sys.exit()

app = QApplication([])
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("tools.db")
db.open()
model = QSqlTableModel(None, db)
model.setTable("tb_tools")
model.select()
model.setHeaderData(0, Qt.Horizontal, "구분")
model.setHeaderData(1, Qt.Horizontal, "순서")
model.setHeaderData(2, Qt.Horizontal, "작업명")
model.setHeaderData(3, Qt.Horizontal, "작업데이터")
model.setHeaderData(4, Qt.Horizontal, "등록일시")
view = QTableView()
view.setModel(model)
view.show()
app.exec_()