import sqlite3
import os


def delete_database():
    # Удаляем файл базы данных, если он существует
    if os.path.exists("database.db"):
        os.remove("database.db")
        print("Старая база данных удалена.")
    else:
        print("База данных не найдена.")


def create_database():
    # Подключение или создание нового файла базы данных
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Создание таблицы records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    )
    """)

    # Добавление тестовых данных
    cursor.executemany("""
    INSERT INTO records (user_id, title, body) VALUES (?, ?, ?)
    """, [
        (1, "Первая запись", "Тело первой записи"),
        (2, "Вторая запись", "Тело второй записи"),
        (3, "Третья запись", "Тело третьей записи")
    ])

    # Сохранение изменений и закрытие подключения
    conn.commit()
    conn.close()

    print("База данных успешно создана и заполнена тестовыми данными!")


if __name__ == "__main__":
    # Сначала удалим старую базу данных
    delete_database()

    # Создадим новую базу данных
    create_database()
