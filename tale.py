import sqlite3

def alter_database():
    # Подключение к базе данных
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Добавление новых столбцов в таблицу records
    cursor.execute("ALTER TABLE records ADD COLUMN user_id TEXT NOT NULL DEFAULT 'default_user'")
    cursor.execute("ALTER TABLE records ADD COLUMN body TEXT NOT NULL DEFAULT 'default_body'")

    # Сохранение изменений и закрытие подключения
    conn.commit()
    conn.close()

    print("Таблица успешно обновлена!")

if __name__ == "__main__":
    alter_database()
