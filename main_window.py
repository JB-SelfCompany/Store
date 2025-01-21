from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QGridLayout, QMessageBox, QDialog,
    QHeaderView, QTabWidget, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки главного окна
        self.setWindowTitle("Продуктовый магазин")
        self.setMinimumSize(1000, 700)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Основная вкладка
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.tabs.addTab(self.main_widget, "Управление продуктами")
        
        # Вкладка аналитики
        self.analytics_widget = QWidget()
        self.analytics_widget.setStyleSheet("""
            background-color: #2D2D2D;
            color: white;
        """)
        self.analytics_layout = QVBoxLayout()
        self.analytics_widget.setLayout(self.analytics_layout)
        self.tabs.addTab(self.analytics_widget, "Аналитика")
        
        # Инициализация интерфейса
        self.init_ui()
        
        # Подключение к базе данных
        self.db_connect()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Заголовок
        title = QLabel("Управление продуктами")
        title.setFont(QFont("Arial", 16))
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title, 0, 0, 1, 2)
        
        # Таблица продуктов
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Код", "Название", "Упаковка", "Дата поступления",
            "Срок хранения", "Объем закупки", "Объем продажи", "Цена", "Скидка"
        ])
        self.table.setSortingEnabled(True)
        
        # Настройка таблицы
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.table, 1, 0, 1, 2)
        
        # Панель управления
        control_panel = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_product)
        
        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_product)
        
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_product)
        
        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.search_product)
        
        control_panel.addWidget(self.add_btn)
        control_panel.addWidget(self.edit_btn)
        control_panel.addWidget(self.delete_btn)
        control_panel.addWidget(self.search_btn)
        
        self.main_layout.addLayout(control_panel, 2, 0, 1, 2)
        
        # Кнопка "Показать все"
        self.show_all_btn = QPushButton("Показать все")
        self.show_all_btn.clicked.connect(self.show_all_products)
        self.main_layout.addWidget(self.show_all_btn, 3, 0, 1, 2)
        
        # Контейнеры для графиков
        self.chart_container = QWidget()
        self.chart_container.setStyleSheet("""
            background-color: #2D2D2D;
            padding: 10px;
            color: white;
        """)
        # Динамическая высота контейнера
        
        # Добавляем скролл
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.chart_container)
        
        self.chart_layout = QVBoxLayout()
        self.chart_layout.setSpacing(20)
        self.chart_layout.setContentsMargins(10, 10, 10, 10)
        self.chart_container.setLayout(self.chart_layout)
        
        self.analytics_layout.addWidget(scroll)
        
        # График тренда дохода
        self.figure1 = plt.Figure(facecolor='#3A3A3A')
        self.figure1.patch.set_alpha(0.0)
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setMinimumSize(600, 400)
        self.figure1.subplots_adjust(bottom=0.3, left=0.15)
        self.canvas1.setStyleSheet("""
            background-color: #3A3A3A;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 15px;
            color: white;
        """)
        
        # Добавляем заголовок
        ax1 = self.figure1.add_subplot(111)
        ax1.set_title("Тренд дохода по месяцам", color='white', pad=20)
        self.chart_layout.addWidget(self.canvas1)
        
        # График топ продаж
        self.figure2 = plt.Figure(facecolor='#3A3A3A')
        self.figure2.patch.set_alpha(0.0)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setMinimumSize(600, 400)
        self.figure2.subplots_adjust(bottom=0.3, left=0.15)
        self.canvas2.setStyleSheet("""
            background-color: #3A3A3A;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 15px;
            color: white;
        """)
        
        # Добавляем заголовок
        ax2 = self.figure2.add_subplot(111)
        ax2.set_title("Топ 5 продаваемых продуктов", color='white', pad=20)
        self.chart_layout.addWidget(self.canvas2)
        
        # Круговая диаграмма распределения запасов
        self.figure3 = plt.Figure(facecolor='#3A3A3A')
        self.figure3.patch.set_alpha(0.0)
        self.canvas3 = FigureCanvas(self.figure3)
        self.canvas3.setMinimumSize(600, 400)
        self.figure3.subplots_adjust(bottom=0.3, left=0.15)
        self.canvas3.setStyleSheet("""
            background-color: #3A3A3A;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 15px;
            color: white;
        """)
        
        # Добавляем заголовок
        ax3 = self.figure3.add_subplot(111)
        ax3.set_title("Распределение запасов", color='white', pad=20)
        self.chart_layout.addWidget(self.canvas3)
        
        # Настройка растяжения
        self.analytics_layout.setContentsMargins(0, 0, 0, 0)
        self.analytics_layout.setSpacing(0)
        
    def show_all_products(self):
        """Показать все продукты"""
        self.update_table()
        
    def db_connect(self):
        """Подключение к базе данных"""
        self.conn = sqlite3.connect('store.db')
        self.cursor = self.conn.cursor()
        
        # Создание таблицы, если она не существует
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                package TEXT,
                receipt_date TEXT,
                storage_days INTEGER,
                purchase_volume REAL,
                sales_volume REAL,
                price REAL
            )
        ''')
        self.conn.commit()
        # Первое обновление таблицы и графиков после подключения к БД
        self.update_table()
        self.update_charts()
        
    def update_table(self):
        """Обновление данных в таблице"""
        self.table.setRowCount(0)
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            # Get discount info if applicable
            discounted = next((p for p in self.calculate_discounts() if p['id'] == row[0]), None)
            
            for col in range(len(row)):
                value = row[col]
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Apply discount to price column
                if col == 7 and discounted:
                    item.setText(f"{discounted['discounted_price']:.2f} ₽")
                    item.setBackground(Qt.yellow)
                    item.setToolTip(f"Скидка {discounted['discount_percent']}% (было {discounted['original_price']} ₽)")
                
                self.table.setItem(row_position, col, item)
            
            # Add discount percentage
            if discounted:
                discount_item = QTableWidgetItem(f"{discounted['discount_percent']}%")
                discount_item.setBackground(Qt.yellow)
            else:
                discount_item = QTableWidgetItem("0%")
            discount_item.setFlags(discount_item.flags() ^ Qt.ItemIsEditable)
            discount_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_position, 8, discount_item)
                
    def add_product(self):
        """Добавление нового продукта"""
        from product_dialog import ProductDialog
        
        dialog = ProductDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            
            self.cursor.execute('''
                INSERT INTO products (
                    name, package, receipt_date, 
                    storage_days, purchase_volume, 
                    sales_volume, price
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['name'], data['package'], data['receipt_date'],
                data['storage_days'], data['purchase_volume'],
                data['sales_volume'], data['price']
            ))
            self.conn.commit()
            self.update_table()
            self.update_charts()
            
    def edit_product(self):
        """Редактирование продукта"""
        from product_dialog import ProductDialog
        
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите продукт для редактирования")
            return
            
        product_id = self.table.item(selected, 0).text()
        
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = self.cursor.fetchone()
        
        if not product:
            QMessageBox.warning(self, "Ошибка", "Продукт не найден")
            return
            
        data = {
            'name': product[1],
            'package': product[2],
            'receipt_date': product[3],
            'storage_days': product[4],
            'purchase_volume': product[5],
            'sales_volume': product[6],
            'price': product[7]
        }
        
        dialog = ProductDialog(self, data)
        if dialog.exec() == QDialog.Accepted:
            new_data = dialog.get_data()
            
            self.cursor.execute('''
                UPDATE products SET
                    name = ?,
                    package = ?,
                    receipt_date = ?,
                    storage_days = ?,
                    purchase_volume = ?,
                    sales_volume = ?,
                    price = ?
                WHERE id = ?
            ''', (
                new_data['name'], new_data['package'], new_data['receipt_date'],
                new_data['storage_days'], new_data['purchase_volume'],
                new_data['sales_volume'], new_data['price'], product_id
            ))
            self.conn.commit()
            self.update_table()
            self.update_charts()
            
    def delete_product(self):
        """Удаление продукта"""
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите продукт для удаления")
            return
            
        product_id = self.table.item(selected, 0).text()
        
        confirm = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить этот продукт?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
            self.update_table()
            self.update_charts()
            
    def search_product(self):
        """Поиск продукта"""
        from PySide6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(
            self,
            "Поиск продукта",
            "Введите название продукта:"
        )
        
        if ok and name:
            self.cursor.execute(
                "SELECT * FROM products WHERE name LIKE ?",
                (f"%{name}%",)
            )
            rows = self.cursor.fetchall()
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                for col, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.table.setItem(row_position, col, item)
                    
    def calculate_income_trend(self):
        """Расчет тренда дохода по месяцам"""
        self.cursor.execute('''
            SELECT strftime('%Y-%m', receipt_date) as month,
                   SUM((sales_volume * price) - (purchase_volume * price * 0.8)) as income
            FROM products
            GROUP BY month
            ORDER BY month
        ''')
        return self.cursor.fetchall()

    def predict_future_income(self, months=3):
        """Прогнозирование дохода на следующие месяцы"""
        data = self.calculate_income_trend()
        if not data:
            return []
            
        # Преобразование данных
        dates = [datetime.strptime(row[0], '%Y-%m') for row in data]
        incomes = [row[1] for row in data]
        
        # Преобразование дат в числовой формат
        x = np.array([(d.year * 12 + d.month) for d in dates]).reshape(-1, 1)
        y = np.array(incomes)
        
        # Обучение модели
        model = LinearRegression()
        model.fit(x, y)
        
        # Прогнозирование
        predictions = []
        last_date = dates[-1]
        for i in range(1, months + 1):
            next_month = last_date + timedelta(days=30*i)
            x_pred = np.array([[next_month.year * 12 + next_month.month]])
            y_pred = model.predict(x_pred)
            predictions.append((next_month.strftime('%Y-%m'), max(0, y_pred[0])))
            
        return predictions

    def calculate_discounts(self):
        """Рассчет скидок для товаров, пролежавших более половины срока хранения"""
        self.cursor.execute('''
            SELECT id, name, price, receipt_date, storage_days
            FROM products
            WHERE
                julianday('now') - julianday(receipt_date) > storage_days / 2
                AND purchase_volume > sales_volume
        ''')
        products = self.cursor.fetchall()
        
        discounted_products = []
        for product in products:
            product_id, name, price, receipt_date, storage_days = product
            days_in_storage = (datetime.now() - datetime.strptime(receipt_date, '%Y-%m-%d')).days
            discount_percent = min(100, int((days_in_storage / storage_days) * 100))
            discounted_price = price * (1 - discount_percent/100)
            discounted_products.append({
                'id': product_id,
                'name': name,
                'original_price': price,
                'discounted_price': discounted_price,
                'discount_percent': discount_percent
            })
            
        return discounted_products

    def update_charts(self):
        """Обновление графиков"""
        # Clear and reinitialize figures
        for fig in [self.figure1, self.figure2, self.figure3]:
            fig.clf()
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2D2D2D')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        # График тренда дохода
        ax1 = self.figure1.add_subplot(111)
        self.figure1.subplots_adjust(left=0.15, bottom=0.35, right=0.95, top=0.85)
        income_data = self.calculate_income_trend()
        plt.setp(ax1.get_xticklabels(), rotation=30, ha='right')
        if income_data:
            months = [row[0] for row in income_data]
            incomes = [row[1] for row in income_data]
            
            ax1.plot(months, incomes, marker='o', color='#1f77b4')
            ax1.set_title("Тренд дохода по месяцам", color='white')
            ax1.set_ylabel("Доход", color='white')
            ax1.tick_params(axis='x', rotation=45, colors='white')
            ax1.tick_params(axis='y', colors='white')
            
            # Прогноз на следующие 3 месяца
            predictions = self.predict_future_income()
            if predictions:
                pred_months = [row[0] for row in predictions]
                pred_incomes = [row[1] for row in predictions]
                ax1.plot(pred_months, pred_incomes, 'r--', marker='o', label='Прогноз')
                ax1.legend(facecolor='#3A3A3A', edgecolor='white', labelcolor='white')
        
        # График самых продаваемых продуктов
        ax2 = self.figure2.add_subplot(111)
        self.figure2.subplots_adjust(left=0.15, bottom=0.4, right=0.95, top=0.85)
        self.cursor.execute('''
            SELECT name, sales_volume 
            FROM products 
            ORDER BY sales_volume DESC 
            LIMIT 5
        ''')
        top_products = self.cursor.fetchall()
        
        if top_products:
            names = [p[0] for p in top_products]
            sales = [p[1] for p in top_products]
            ax2.bar(names, sales, color='#1f77b4')
            ax2.set_title("Топ 5 продаваемых продуктов", color='white', pad=20)
            ax2.set_ylabel("Объем продаж (кг)", color='white')
            ax2.tick_params(axis='x', rotation=30, colors='white')
            ax2.tick_params(axis='y', colors='white')
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f} кг'))
            
        # Круговая диаграмма распределения запасов
        ax3 = self.figure3.add_subplot(111)
        self.cursor.execute('''
            SELECT name, purchase_volume - sales_volume 
            FROM products 
            WHERE purchase_volume - sales_volume > 0
        ''')
        stock = self.cursor.fetchall()
        
        if stock:
            names = [s[0] for s in stock]
            volumes = [s[1] for s in stock]
            
            ax3.pie(volumes, labels=names, autopct='%1.1f%%', 
                   textprops={'color': 'white'})
            ax3.set_title("Распределение запасов", color='white', pad=20)
            
        # Настройка цветов для темной темы
        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor('#2D2D2D')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white') 
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            plt.tight_layout()
