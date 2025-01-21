from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QDateEdit, QDoubleSpinBox, 
    QSpinBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIntValidator

class ProductDialog(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        
        self.setWindowTitle("Добавление/Редактирование продукта")
        self.setModal(True)
        
        # Основной layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название продукта")
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.name_input)
        
        self.package_input = QLineEdit()
        self.package_input.setPlaceholderText("Тип упаковки")
        layout.addWidget(QLabel("Упаковка:"))
        layout.addWidget(self.package_input)
        
        self.receipt_date = QDateEdit()
        self.receipt_date.setCalendarPopup(True)
        self.receipt_date.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Дата поступления:"))
        layout.addWidget(self.receipt_date)
        
        self.storage_days = QSpinBox()
        self.storage_days.setRange(1, 365)
        self.storage_days.setValue(30)
        layout.addWidget(QLabel("Срок хранения (дней):"))
        layout.addWidget(self.storage_days)
        
        self.purchase_volume = QDoubleSpinBox()
        self.purchase_volume.setRange(0, 1000000)
        self.purchase_volume.setValue(0)
        self.purchase_volume.setPrefix("кг: ")
        layout.addWidget(QLabel("Объем закупки:"))
        layout.addWidget(self.purchase_volume)
        
        self.sales_volume = QDoubleSpinBox()
        self.sales_volume.setRange(0, 1000000)
        self.sales_volume.setValue(0)
        self.sales_volume.setPrefix("кг: ")
        layout.addWidget(QLabel("Объем продажи:"))
        layout.addWidget(self.sales_volume)
        
        self.price = QDoubleSpinBox()
        self.price.setRange(0, 1000000)
        self.price.setValue(0)
        self.price.setPrefix("₽: ")
        layout.addWidget(QLabel("Цена:"))
        layout.addWidget(self.price)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.validate_and_accept)
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        # Если переданы данные продукта - заполняем поля
        if product_data:
            self.fill_form(product_data)
            
    def fill_form(self, data):
        """Заполнение формы данными продукта"""
        self.name_input.setText(data.get('name', ''))
        self.package_input.setText(data.get('package', ''))
        self.receipt_date.setDate(QDate.fromString(data.get('receipt_date', ''), 'yyyy-MM-dd'))
        self.storage_days.setValue(data.get('storage_days', 30))
        self.purchase_volume.setValue(data.get('purchase_volume', 0))
        self.sales_volume.setValue(data.get('sales_volume', 0))
        self.price.setValue(data.get('price', 0))
        
    def get_data(self):
        """Получение данных из формы"""
        return {
            'name': self.name_input.text().strip(),
            'package': self.package_input.text().strip(),
            'receipt_date': self.receipt_date.date().toString('yyyy-MM-dd'),
            'storage_days': self.storage_days.value(),
            'purchase_volume': self.purchase_volume.value(),
            'sales_volume': self.sales_volume.value(),
            'price': self.price.value()
        }
        
    def validate_and_accept(self):
        """Валидация данных и закрытие формы"""
        data = self.get_data()
        
        if not data['name']:
            QMessageBox.warning(self, "Ошибка", "Название продукта не может быть пустым")
            return
            
        if data['purchase_volume'] < data['sales_volume']:
            QMessageBox.warning(self, "Ошибка", "Объем продажи не может превышать объем закупки")
            return
            
        self.accept()
