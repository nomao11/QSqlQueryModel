import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLineEdit, QTableView, QMessageBox, QHBoxLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

class TeacherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Teachers CRUD Application")
        self.setGeometry(100, 100, 600, 400)

        self.model = QSqlQueryModel()
        self.initUI()
        self.createConnection()
        self.loadData()

    def initUI(self):
        layout = QVBoxLayout()
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Введите имя учителя")
        layout.addWidget(self.name_input)
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить учителя", self)
        self.add_button.clicked.connect(self.addTeacher)
        button_layout.addWidget(self.add_button)
        self.update_button = QPushButton("Обновить учителя", self)
        self.update_button.clicked.connect(self.updateTeacher)
        button_layout.addWidget(self.update_button)
        self.delete_button = QPushButton("Удалить учителя", self)
        self.delete_button.clicked.connect(self.deleteTeacher)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)
        self.table_view = QTableView(self)
        self.table_view.clicked.connect(self.onTableClick)
        layout.addWidget(self.table_view)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def createConnection(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("teachers.db")
        if not self.db.open():
            QMessageBox.critical(None, "Ошибка базы данных", "Не удалось открыть базу данных.")
            sys.exit(1)
        query = QSqlQuery()
        query.exec_("""CREATE TABLE IF NOT EXISTS Teachers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)""")

    def loadData(self):
        self.model.setQuery("SELECT * FROM Teachers")
        self.table_view.setModel(self.model)

    def onTableClick(self, index):
        selected_row = index.row()
        name = self.model.data(self.model.index(selected_row, 1))
        self.name_input.setText(name)

    def addTeacher(self):
        name = self.name_input.text()
        if name:
            query = QSqlQuery()
            query.prepare("INSERT INTO Teachers (name) VALUES (:name)")
            query.bindValue(":name", name)
            if query.exec_():
                self.loadData()
                self.name_input.clear()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить учителя.")

    def updateTeacher(self):
        selected_row = self.table_view.currentIndex().row()
        if selected_row >= 0:
            teacher_id = self.model.data(self.model.index(selected_row, 0))
            name = self.name_input.text()
            if name:
                query = QSqlQuery()
                query.prepare("UPDATE Teachers SET name = :name WHERE id = :id")
                query.bindValue(":name", name)
                query.bindValue(":id", teacher_id)
                if query.exec_():
                    self.loadData()
                    self.name_input.clear()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось обновить учителя.")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите учителя для обновления.")

    def deleteTeacher(self):
        selected_row = self.table_view.currentIndex().row()
        if selected_row >= 0:
            teacher_id = self.model.data(self.model.index(selected_row, 0))
            query = QSqlQuery()
            query.prepare("DELETE FROM Teachers WHERE id = :id")
            query.bindValue(":id", teacher_id)
            if query.exec_():
                self.loadData()
                self.name_input.clear()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить учителя.")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите учителя для удаления.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherApp()
    window.show()
    sys.exit(app.exec_())