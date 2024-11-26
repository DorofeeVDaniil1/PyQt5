import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QTableView, QWidget, QMessageBox, QInputDialog
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Приложение на PyQt")
        self.setGeometry(200, 200, 800, 600)

        # Настройка базы данных
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database.db")
        if not self.db.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных")
            sys.exit(1)

        # Модель данных для таблицы
        self.model = QSqlTableModel(self)
        self.model.setTable("records")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        # Элементы интерфейса
        self.table = QTableView()
        self.table.setModel(self.model)

        # Добавляем таблицу с нужными полями
        self.table.setColumnHidden(0, False)  # Скрываем ID, если не нужно показывать
        self.table.setColumnHidden(1, False)  # Скрываем User ID, если не нужно показывать

        # Поле поиска
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск по заголовку...")
        self.search_field.textChanged.connect(self.search)

        # Кнопки
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.refresh)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_record)

        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.search_field)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search(self):
        filter_text = self.search_field.text()
        self.model.setFilter(f"title LIKE '%{filter_text}%'")

    def refresh(self):
        self.model.select()

    def add_record(self):
        title, ok = QInputDialog.getText(self, "Добавить запись", "Введите заголовок:")
        if ok and title.strip():
            user_id, ok_user_id = QInputDialog.getText(self, "Добавить запись", "Введите ID пользователя:")
            if ok_user_id and user_id.strip():
                body, ok_body = QInputDialog.getText(self, "Добавить запись", "Введите текст тела записи:")
                if ok_body and body.strip():
                    query = QSqlQuery()
                    query.prepare("INSERT INTO records (user_id, title, body) VALUES (:user_id, :title, :body)")
                    query.bindValue(":user_id", user_id.strip())
                    query.bindValue(":title", title.strip())
                    query.bindValue(":body", body.strip())
                    if not query.exec():
                        QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись: {query.lastError().text()}")
                    else:
                        self.refresh()
                elif ok_body:
                    QMessageBox.warning(self, "Предупреждение", "Тело записи не может быть пустым!")
            elif ok_user_id:
                QMessageBox.warning(self, "Предупреждение", "ID пользователя не может быть пустым!")
        elif ok:
            QMessageBox.warning(self, "Предупреждение", "Заголовок не может быть пустым!")

    def delete_record(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return
        for index in selected_rows:
            self.model.removeRow(index.row())
        self.model.submitAll()
        self.refresh()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
