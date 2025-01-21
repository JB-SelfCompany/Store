import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from main_window import MainWindow

def get_app_dir():
    """Получаем директорию приложения"""
    if getattr(sys, 'frozen', False):
        # Если приложение собрано
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def setup_database():
    db = QSqlDatabase.addDatabase('QSQLITE')
    
    # Путь к базе данных в директории приложения
    db_path = os.path.join(get_app_dir(), 'app_data.db')
    db.setDatabaseName(db_path)
    
    # Проверяем, нужно ли создавать новую базу данных
    is_new_db = not os.path.exists(db_path)
    
    if not db.open():
        print("Ошибка: Не удалось открыть базу данных")
        return False
        
    if is_new_db:
        # Создаем таблицы для новой базы данных
        query = QSqlQuery()
        if not query.exec("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """):
            print("Ошибка: Не удалось создать таблицу products")
            return False
            
        # Добавляем начальные данные
        if not query.exec("INSERT INTO products (name, price) VALUES ('Пример продукта', 100.0)"):
            print("Ошибка: Не удалось добавить начальные данные")
            
    return True

def main():
    app = QApplication(sys.argv)
    
    if not setup_database():
        sys.exit(1)
        
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
