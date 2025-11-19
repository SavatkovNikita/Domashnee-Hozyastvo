import sqlite3
import os


def create_test_database():
    """Создаем тестовую базу данных"""
    if os.path.exists('storage.db'):
        os.remove('storage.db')

    conn = sqlite3.connect('storage.db')
    cursor = conn.cursor()

    # Создаем таблицы
    cursor.execute('''
        CREATE TABLE User (
            User_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Budget REAL,
            Password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Storage (
            Storage_ID INTEGER PRIMARY KEY,
            Type TEXT NOT NULL,
            Volume REAL NOT NULL,
            User_ID INTEGER,
            FOREIGN KEY (User_ID) REFERENCES User(User_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Item (
            Item_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Storage_Item (
            ID INTEGER PRIMARY KEY,
            ID_Item INTEGER,
            ID_Storage INTEGER,
            FOREIGN KEY (ID_Item) REFERENCES Item(Item_ID),
            FOREIGN KEY (ID_Storage) REFERENCES Storage(Storage_ID)
        )
    ''')

    # Добавляем тестовые данные
    cursor.execute("INSERT INTO User VALUES (1, 'Иван Иванов', 50000.0, 'pass123')")
    cursor.execute("INSERT INTO User VALUES (2, 'Мария Петрова', 75000.0, 'pass456')")

    cursor.execute("INSERT INTO Storage VALUES (1, 'Холодильник', 300.5, 1)")
    cursor.execute("INSERT INTO Storage VALUES (2, 'Кухонный шкаф', 150.0, 1)")
    cursor.execute("INSERT INTO Storage VALUES (3, 'Морозильная камера', 200.0, 2)")

    cursor.execute("INSERT INTO Item VALUES (1, 'Молоко')")
    cursor.execute("INSERT INTO Item VALUES (2, 'Хлеб')")
    cursor.execute("INSERT INTO Item VALUES (3, 'Мясо')")
    cursor.execute("INSERT INTO Item VALUES (4, 'Овощи')")

    cursor.execute("INSERT INTO Storage_Item VALUES (1, 1, 1)")
    cursor.execute("INSERT INTO Storage_Item VALUES (2, 2, 1)")
    cursor.execute("INSERT INTO Storage_Item VALUES (3, 3, 3)")
    cursor.execute("INSERT INTO Storage_Item VALUES (4, 4, 2)")

    conn.commit()
    conn.close()
    print("Тестовая база данных создана!")


if __name__ == "__main__":
    create_test_database()