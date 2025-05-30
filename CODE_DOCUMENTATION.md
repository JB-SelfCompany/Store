# РУКОВОДСТВО ПРОГРАММИСТА
## Система управления продуктовым магазином

### ГОСТ 19.504-79

---

## 1. НАЗНАЧЕНИЕ И УСЛОВИЯ ПРИМЕНЕНИЯ ПРОГРАММЫ

### 1.1 Назначение программы
Программа "Система управления продуктовым магазином" предназначена для автоматизации учета товаров в продуктовом магазине, включая:
- Ведение базы данных продуктов
- Учет поступления и продажи товаров
- Аналитику продаж и прогнозирование доходов
- Визуализацию данных

### 1.2 Область применения
- Малые и средние продуктовые магазины
- Склады продовольственных товаров
- Торговые точки с ограниченным ассортиментом

### 1.3 Технические требования
**Минимальные системные требования:**
- Операционная система: Windows 10/11 (64-bit)
- Оперативная память: 4 ГБ
- Свободное место на диске: 200 МБ
- Разрешение экрана: 1024x768

**Программные зависимости:**
- Python 3.8+
- PySide6
- matplotlib
- scikit-learn
- numpy

## 2. ХАРАКТЕРИСТИКА ПРОГРАММЫ

### 2.1 Режим работы
- Интерактивный режим с графическим интерфейсом
- Локальная база данных SQLite
- Однопользовательский режим

### 2.2 Показатели производительности
- Время запуска: не более 5 секунд
- Время отклика интерфейса: не более 1 секунды
- Максимальное количество записей: до 100,000 продуктов
- Объем базы данных: до 500 МБ

### 2.3 Функциональные характеристики
- CRUD операции с продуктами
- Поиск и фильтрация данных
- Построение аналитических графиков
- Прогнозирование доходов на основе машинного обучения

## 3. ОБРАЩЕНИЕ К ПРОГРАММЕ

### 3.1 Способы запуска

#### 3.1.1 Запуск из исходного кода
```bash
python main.py
```

#### 3.1.2 Запуск исполняемого файла
```bash
store-windows.exe
```

### 3.2 Параметры запуска
Программа не принимает параметры командной строки.

### 3.3 Инициализация
При первом запуске автоматически создается:
- База данных SQLite: `products.db`
- Директория приложения в `%APPDATA%/ProductStore`

## 4. ВХОДНЫЕ И ВЫХОДНЫЕ ДАННЫЕ

### 4.1 Входные данные

#### 4.1.1 Структура данных продукта
```python
Product = {
    'name': str,           # Название продукта (обязательно)
    'package': str,        # Тип упаковки (опционально)
    'receipt_date': str,   # Дата поступления (ДД.ММ.ГГГГ)
    'storage_days': int,   # Срок хранения в днях
    'purchase_volume': float,  # Объем закупки (кг)
    'sales_volume': float,     # Объем продажи (кг)
    'price': float        # Цена за единицу (руб)
}
```

#### 4.1.2 Ограничения входных данных
- `name`: строка длиной от 1 до 255 символов
- `receipt_date`: дата в формате ДД.ММ.ГГГГ
- `storage_days`: целое число от 1 до 3650
- `purchase_volume`: положительное число с плавающей точкой
- `sales_volume`: число от 0 до `purchase_volume`
- `price`: положительное число с плавающей точкой

### 4.2 Выходные данные

#### 4.2.1 База данных SQLite
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    package TEXT,
    receipt_date TEXT,
    storage_days INTEGER,
    purchase_volume REAL,
    sales_volume REAL,
    price REAL
);
```

#### 4.2.2 Аналитические данные
- Графики трендов доходов (PNG/SVG)
- Диаграммы распределения продаж
- Прогнозы доходов на 3 месяца

## 5. СООБЩЕНИЯ

### 5.1 Информационные сообщения

#### 5.1.1 Успешные операции
```
"Продукт успешно добавлен"
Действие: Продолжить работу
```

```
"Данные сохранены"
Действие: Продолжить работу
```

### 5.2 Предупреждающие сообщения

#### 5.2.1 Валидация данных
```
"Заполните все обязательные поля"
Действие: Проверить и заполнить поля формы
```

```
"Некорректный формат даты. Используйте ДД.ММ.ГГГГ"
Действие: Исправить формат даты
```

```
"Объем продажи не может превышать объем закупки"
Действие: Скорректировать значения
```

### 5.3 Сообщения об ошибках

#### 5.3.1 Ошибки базы данных
```
"Ошибка подключения к базе данных"
Действие: Перезапустить программу, проверить права доступа
```

```
"Продукт с таким названием уже существует"
Действие: Изменить название или отредактировать существующий продукт
```

#### 5.3.2 Системные ошибки
```
"Недостаточно памяти для выполнения операции"
Действие: Закрыть лишние приложения, перезапустить программу
```

```
"Ошибка создания графика"
Действие: Проверить наличие данных, перезапустить программу
```

---

## ПРИЛОЖЕНИЯ

### Приложение А. Структура модулей

#### А.1 main.py
**Назначение:** Точка входа в приложение и инициализация базы данных

**Функции:**
- `get_app_dir()` - получение директории приложения
- `setup_database()` - настройка и инициализация базы данных SQLite
- `main()` - точка входа в приложение

**Входные параметры:** Отсутствуют
**Выходные данные:** Код завершения программы (0 - успех, 1 - ошибка)

#### А.2 main_window.py
**Назначение:** Основной модуль GUI и бизнес-логики

**Класс MainWindow:**
- Наследует: `QMainWindow`
- Назначение: Главное окно приложения

**Основные методы:**
```python
def __init__(self) -> None
    # Инициализация главного окна
    
def init_ui(self) -> None
    # Настройка пользовательского интерфейса
    
def db_connect(self) -> sqlite3.Connection
    # Подключение к базе данных
    # Возвращает: объект соединения с БД
    
def update_table(self) -> None
    # Обновление таблицы продуктов
    
def add_product(self) -> None
    # Добавление нового продукта
    
def edit_product(self) -> None
    # Редактирование существующего продукта
    
def delete_product(self) -> None
    # Удаление продукта
    
def search_product(self) -> None
    # Поиск продукта по названию
```

**Аналитические методы:**
```python
def calculate_income_trend(self) -> List[float]
    # Расчет тренда дохода
    # Возвращает: список значений дохода по месяцам
    
def predict_future_income(self) -> List[float]
    # Прогнозирование дохода на 3 месяца
    # Возвращает: прогнозные значения дохода
    
def calculate_discounts(self) -> Dict[str, float]
    # Расчет рекомендуемых скидок
    # Возвращает: словарь {название_продукта: размер_скидки}
```

#### А.3 product_dialog.py
**Назначение:** Диалоговое окно для работы с продуктами

**Класс ProductDialog:**
- Наследует: `QDialog`
- Назначение: Форма добавления/редактирования продукта

**Методы:**
```python
def __init__(self, parent=None, product_data=None) -> None
    # Инициализация диалога
    # parent: родительское окно
    # product_data: данные продукта для редактирования
    
def fill_form(self, data: Dict) -> None
    # Заполнение формы данными продукта
    # data: словарь с данными продукта
    
def get_data(self) -> Dict
    # Получение данных из формы
    # Возвращает: словарь с данными продукта
    
def validate_and_accept(self) -> None
    # Валидация данных и закрытие формы
```

### Приложение Б. Схема базы данных

#### Б.1 Таблица products
```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Уникальный идентификатор
    name TEXT NOT NULL,                    -- Название продукта
    package TEXT,                          -- Тип упаковки
    receipt_date TEXT,                     -- Дата поступления
    storage_days INTEGER,                  -- Срок хранения (дни)
    purchase_volume REAL,                  -- Объем закупки (кг)
    sales_volume REAL,                     -- Объем продажи (кг)
    price REAL                            -- Цена за единицу (руб)
);
```

#### Б.2 Индексы
```sql
CREATE INDEX IF NOT EXISTS idx_product_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_receipt_date ON products(receipt_date);
```

### Приложение В. Алгоритмы

#### В.1 Алгоритм прогнозирования доходов
```python
# Использует линейную регрессию из scikit-learn
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_income(historical_data):
    """
    Прогнозирование доходов на основе исторических данных
    
    Входные данные:
    - historical_data: список доходов по месяцам
    
    Выходные данные:
    - прогноз на 3 месяца вперед
    """
    if len(historical_data) < 3:
        return [0, 0, 0]  # Недостаточно данных
    
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = np.array(historical_data)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Прогноз на 3 месяца
    future_months = np.array([
        len(historical_data),
        len(historical_data) + 1,
        len(historical_data) + 2
    ]).reshape(-1, 1)
    
    return model.predict(future_months).tolist()
```

#### В.2 Алгоритм расчета скидок
```python
def calculate_discount(purchase_volume, sales_volume, storage_days):
    """
    Расчет рекомендуемой скидки на основе остатков и срока хранения
    
    Входные данные:
    - purchase_volume: объем закупки
    - sales_volume: объем продажи
    - storage_days: срок хранения
    
    Выходные данные:
    - размер скидки в процентах (0-50%)
    """
    remaining = purchase_volume - sales_volume
    if remaining <= 0:
        return 0
    
    # Базовая скидка на основе остатков
    base_discount = min(remaining / purchase_volume * 30, 30)
    
    # Дополнительная скидка для скоропортящихся товаров
    if storage_days <= 7:
        base_discount += 20
    elif storage_days <= 30:
        base_discount += 10
    
    return min(base_discount, 50)  # Максимум 50%
```

### Приложение Г. Примеры использования API

#### Г.1 Добавление продукта программно
```python
import sqlite3
from datetime import datetime

def add_product_api(name, package, storage_days, purchase_volume, price):
    """
    Программное добавление продукта в базу данных
    """
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    receipt_date = datetime.now().strftime('%d.%m.%Y')
    
    cursor.execute('''
        INSERT INTO products 
        (name, package, receipt_date, storage_days, purchase_volume, sales_volume, price)
        VALUES (?, ?, ?, ?, ?, 0, ?)
    ''', (name, package, receipt_date, storage_days, purchase_volume, price))
    
    conn.commit()
    conn.close()
    
    return cursor.lastrowid

# Пример использования
product_id = add_product_api(
    name="Молоко 3.2%",
    package="Пластиковая бутылка 1л",
    storage_days=7,
    purchase_volume=50.0,
    price=65.50
)
```

#### Г.2 Получение аналитических данных
```python
def get_analytics_data():
    """
    Получение данных для аналитики
    """
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # Топ продаж
    cursor.execute('''
        SELECT name, sales_volume 
        FROM products 
        ORDER BY sales_volume DESC 
        LIMIT 5
    ''')
    top_sales = cursor.fetchall()
    
    # Общий доход
    cursor.execute('''
        SELECT SUM((sales_volume * price) - (purchase_volume * price * 0.8))
        FROM products
    ''')
    total_income = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'top_sales': top_sales,
        'total_income': total_income
    }