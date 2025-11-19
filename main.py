import sqlite3
import json
import csv
import xml.etree.ElementTree as ET
import os
from datetime import datetime


class DataExporter:
    def __init__(self, db_path='storage.db'):
        self.db_path = db_path
        self.output_dir = 'out'
        self.create_output_dir()

    def create_output_dir(self):
        """Создает папку out если её нет"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Создана папка {self.output_dir}")

    def get_connection(self):
        """Возвращает соединение с базой данных"""
        return sqlite3.connect(self.db_path)

    def fetch_storage_data(self):
        """Извлекает данные о хранилищах с связанными данными"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Получаем основные данные о хранилищах с информацией о пользователе
        cursor.execute('''
            SELECT 
                s.Storage_ID,
                s.Type,
                s.Volume,
                u.User_ID,
                u.Name as User_Name,
                u.Budget
            FROM Storage s
            LEFT JOIN User u ON s.User_ID = u.User_ID
        ''')

        storage_data = []
        for row in cursor.fetchall():
            storage_id, type_, volume, user_id, user_name, budget = row

            # Получаем предметы в этом хранилище
            cursor.execute('''
                SELECT i.Item_ID, i.Name
                FROM Storage_Item si
                JOIN Item i ON si.ID_Item = i.Item_ID
                WHERE si.ID_Storage = ?
            ''', (storage_id,))

            items = [{'item_id': item_id, 'name': name}
                     for item_id, name in cursor.fetchall()]

            storage_record = {
                'storage_id': storage_id,
                'type': type_,
                'volume': volume,
                'user': {
                    'user_id': user_id,
                    'name': user_name,
                    'budget': budget
                } if user_id else None,
                'items': items
            }
            storage_data.append(storage_record)

        conn.close()
        return storage_data

    def export_to_json(self, data):
        """Экспорт в JSON"""
        output_path = os.path.join(self.output_dir, 'data.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные экспортированы в {output_path}")

    def export_to_csv(self, data):
        """Экспорт в CSV"""
        output_path = os.path.join(self.output_dir, 'data.csv')

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)

            # Заголовки
            writer.writerow([
                'Storage_ID', 'Type', 'Volume',
                'User_ID', 'User_Name', 'User_Budget',
                'Items'
            ])

            # Данные
            for record in data:
                items_str = '; '.join([f"{item['name']}" for item in record['items']])
                user = record.get('user', {})

                writer.writerow([
                    record['storage_id'],
                    record['type'],
                    record['volume'],
                    user.get('user_id', ''),
                    user.get('name', ''),
                    user.get('budget', ''),
                    items_str
                ])

        print(f"Данные экспортированы в {output_path}")

    def export_to_xml(self, data):
        """Экспорт в XML"""
        root = ET.Element('Storages')

        for record in data:
            storage_elem = ET.SubElement(root, 'Storage')

            ET.SubElement(storage_elem, 'Storage_ID').text = str(record['storage_id'])
            ET.SubElement(storage_elem, 'Type').text = record['type']
            ET.SubElement(storage_elem, 'Volume').text = str(record['volume'])

            if record['user']:
                user_elem = ET.SubElement(storage_elem, 'User')
                ET.SubElement(user_elem, 'User_ID').text = str(record['user']['user_id'])
                ET.SubElement(user_elem, 'Name').text = record['user']['name']
                ET.SubElement(user_elem, 'Budget').text = str(record['user']['budget'])

            if record['items']:
                items_elem = ET.SubElement(storage_elem, 'Items')
                for item in record['items']:
                    item_elem = ET.SubElement(items_elem, 'Item')
                    ET.SubElement(item_elem, 'Item_ID').text = str(item['item_id'])
                    ET.SubElement(item_elem, 'Name').text = item['name']

        tree = ET.ElementTree(root)
        output_path = os.path.join(self.output_dir, 'data.xml')
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"Данные экспортированы в {output_path}")

    def export_to_yaml(self, data):
        """Экспорт в YAML - упрощенная версия без библиотеки"""
        output_path = os.path.join(self.output_dir, 'data.yaml')

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Данные хранилищ\n")
            for record in data:
                f.write(f"- storage_id: {record['storage_id']}\n")
                f.write(f"  type: {record['type']}\n")
                f.write(f"  volume: {record['volume']}\n")

                if record['user']:
                    f.write(f"  user:\n")
                    f.write(f"    user_id: {record['user']['user_id']}\n")
                    f.write(f"    name: {record['user']['name']}\n")
                    f.write(f"    budget: {record['user']['budget']}\n")
                else:
                    f.write(f"  user: null\n")

                f.write(f"  items:\n")
                for item in record['items']:
                    f.write(f"  - item_id: {item['item_id']}\n")
                    f.write(f"    name: {item['name']}\n")
                f.write("\n")

        print(f"Данные экспортированы в {output_path}")

    def export_all_formats(self):
        """Экспортирует данные во всех форматах"""
        print("Извлечение данных из базы...")
        data = self.fetch_storage_data()

        if not data:
            print("Нет данных для экспорта!")
            return

        print(f"Найдено {len(data)} записей")

        self.export_to_json(data)
        self.export_to_csv(data)
        self.export_to_xml(data)
        self.export_to_yaml(data)

        print("\nЭкспорт завершен!")


def main():
    # Сначала создаем тестовую базу (если её нет)
    if not os.path.exists('storage.db'):
        print("Создание тестовой базы данных...")
        from database import create_test_database
        create_test_database()

    # Экспортируем данные
    exporter = DataExporter()
    exporter.export_all_formats()

if __name__ == "__main__":
    main()