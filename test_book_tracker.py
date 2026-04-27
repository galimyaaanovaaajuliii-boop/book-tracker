"""
Модульные тесты для Book Tracker
Тестирование позитивных, негативных и граничных случаев
"""

import unittest
import os
import tempfile
from book_manager import Book, BookManager

class TestBook(unittest.TestCase):
    """Тесты для класса Book"""
    
    def setUp(self):
        self.book = Book("Война и мир", "Лев Толстой", "Роман", 1300)
    
    def test_book_creation(self):
        """Тест создания книги (позитивный)"""
        self.assertEqual(self.book.title, "Война и мир")
        self.assertEqual(self.book.author, "Лев Толстой")
        self.assertEqual(self.book.genre, "Роман")
        self.assertEqual(self.book.pages, 1300)
    
    def test_book_to_dict(self):
        """Тест преобразования в словарь"""
        data = self.book.to_dict()
        self.assertEqual(data['title'], "Война и мир")
        self.assertEqual(data['pages'], 1300)
    
    def test_book_from_dict(self):
        """Тест создания книги из словаря"""
        data = {
            'title': 'Тестовая книга',
            'author': 'Тестовый автор',
            'genre': 'Тестовый жанр',
            'pages': 100
        }
        book = Book.from_dict(data)
        self.assertEqual(book.title, 'Тестовая книга')

class TestBookManager(unittest.TestCase):
    """Тесты для класса BookManager"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = BookManager(self.temp_file.name)
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_add_book_positive(self):
        """Тест успешного добавления книги"""
        result = self.manager.add_book("1984", "Джордж Оруэлл", "Антиутопия", 328)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_books()), 1)
    
    def test_add_book_duplicate(self):
        """Тест предотвращения дубликатов"""
        self.manager.add_book("1984", "Джордж Оруэлл", "Антиутопия", 328)
        result = self.manager.add_book("1984", "Джордж Оруэлл", "Антиутопия", 328)
        self.assertFalse(result)
    
    def test_remove_book_positive(self):
        """Тест успешного удаления книги"""
        self.manager.add_book("Книга 1", "Автор 1", "Жанр 1", 100)
        result = self.manager.remove_book(0)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_books()), 0)
    
    def test_remove_book_invalid_index(self):
        """Тест удаления с неверным индексом"""
        result = self.manager.remove_book(999)
        self.assertFalse(result)
    
    def test_filter_by_genre(self):
        """Тест фильтрации по жанру"""
        self.manager.add_book("Книга 1", "Автор 1", "Фантастика", 100)
        self.manager.add_book("Книга 2", "Автор 2", "Детектив", 150)
        
        filtered = self.manager.filter_by_genre("Фантастика")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].genre, "Фантастика")
    
    def test_filter_by_pages(self):
        """Тест фильтрации по страницам"""
        self.manager.add_book("Книга 1", "Автор 1", "Жанр 1", 100)
        self.manager.add_book("Книга 2", "Автор 2", "Жанр 2", 200)
        self.manager.add_book("Книга 3", "Автор 3", "Жанр 3", 300)
        
        filtered = self.manager.filter_by_pages(150)
        self.assertEqual(len(filtered), 2)
    
    def test_get_unique_genres(self):
        """Тест получения уникальных жанров"""
        self.manager.add_book("Книга 1", "Автор 1", "Фантастика", 100)
        self.manager.add_book("Книга 2", "Автор 2", "Детектив", 150)
        self.manager.add_book("Книга 3", "Автор 3", "Фантастика", 200)
        
        genres = self.manager.get_unique_genres()
        self.assertEqual(set(genres), {"Фантастика", "Детектив"})
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки JSON"""
        self.manager.add_book("Тестовая книга", "Тестовый автор", "Тестовый жанр", 500)
        self.manager.save_books()
        
        new_manager = BookManager(self.temp_file.name)
        self.assertEqual(len(new_manager.get_books()), 1)

def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBook))
    suite.addTests(loader.loadTestsFromTestCase(TestBookManager))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    print(f"Результаты тестирования:")
    print(f"Запущено тестов: {result.testsRun}")
    print(f="="*50)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_tests()
