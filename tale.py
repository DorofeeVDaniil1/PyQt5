import sqlite3

def create_database():
    # Подключение или создание файла базы данных
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Создание таблицы records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL
    )
    """)

    # Добавление тестовых данных
    cursor.executemany("""
    INSERT INTO records (title) VALUES (?)
    """, [
        ("Первая запись",),
        ("Вторая запись",),
        ("Третья запись",)
    ])

    # Сохранение изменений и закрытие подключения
    conn.commit()
    conn.close()

    print("База данных успешно создана и заполнена тестовыми данными!")

if __name__ == "__main__":
    create_database()
