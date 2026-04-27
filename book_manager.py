"""
Модуль для управления коллекцией книг
Содержит логику работы с данными и JSON
"""

import json
import os
from datetime import datetime
from typing import List, Dict

class Book:
    """Класс для представления книги"""
    
    def __init__(self, title: str, author: str, genre: str, pages: int):
        self.title = title.strip()
        self.author = author.strip()
        self.genre = genre.strip()
        self.pages = pages
        self.date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Преобразует книгу в словарь для JSON"""
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'pages': self.pages,
            'date_added': self.date_added
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Создаёт книгу из словаря"""
        book = cls(data['title'], data['author'], data['genre'], data['pages'])
        book.date_added = data.get('date_added', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return book

class BookManager:
    """Класс для управления коллекцией книг"""
    
    def __init__(self, filename: str = "books.json"):
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()
    
    def add_book(self, title: str, author: str, genre: str, pages: int) -> bool:
        """Добавляет новую книгу. Возвращает True если успешно, False если дубликат"""
        # Проверка на дубликат
        for book in self.books:
            if (book.title.lower() == title.lower() and 
                book.author.lower() == author.lower()):
                return False
        
        book = Book(title, author, genre, pages)
        self.books.append(book)
        self.save_books()
        return True
    
    def remove_book(self, index: int) -> bool:
        """Удаляет книгу по индексу"""
        if 0 <= index < len(self.books):
            del self.books[index]
            self.save_books()
            return True
        return False
    
    def get_books(self) -> List[Book]:
        """Возвращает список всех книг"""
        return self.books
    
    def filter_by_genre(self, genre: str) -> List[Book]:
        """Фильтрует книги по жанру"""
        if not genre or genre == "Все жанры":
            return self.books
        return [book for book in self.books if book.genre.lower() == genre.lower()]
    
    def filter_by_pages(self, min_pages: int) -> List[Book]:
        """Фильтрует книги по минимальному количеству страниц"""
        return [book for book in self.books if book.pages > min_pages]
    
    def get_unique_genres(self) -> List[str]:
        """Возвращает список уникальных жанров"""
        genres = set(book.genre for book in self.books)
        return sorted(list(genres))
    
    def save_books(self) -> bool:
        """Сохраняет книги в JSON файл"""
        try:
            data = [book.to_dict() for book in self.books]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False
    
    def load_books(self):
        """Загружает книги из JSON файла"""
        if not os.path.exists(self.filename):
            # Создаём файл с примером данных при первом запуске
            self.books = []
            self.add_example_data()
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.books = [Book.from_dict(item) for item in data]
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            self.books = []
    
    def add_example_data(self):
        """Добавляет примеры книг для демонстрации"""
        example_books = [
            ("Война и мир", "Лев Толстой", "Роман", 1300),
            ("Преступление и наказание", "Фёдор Достоевский", "Роман", 672),
            ("Мастер и Маргарита", "Михаил Булгаков", "Мистика", 480),
            ("1984", "Джордж Оруэлл", "Антиутопия", 328),
            ("Гарри Поттер и философский камень", "Джоан Роулинг", "Фэнтези", 432),
        ]
        for title, author, genre, pages in example_books:
            self.add_book(title, author, genre, pages)
    
    def clear_all_books(self):
        """Очищает все книги (для тестирования)"""
        self.books = []
        self.save_books()
