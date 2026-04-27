"""
Графический интерфейс для Book Tracker
Использует tkinter для создания GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from book_manager import BookManager

class BookTrackerGUI:
    """Основной класс GUI приложения"""
    
    def __init__(self, root):
        self.root = root
        self.book_manager = BookManager()
        
        # Настройка главного окна
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("950x650")
        self.root.resizable(True, True)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка данных
        self.refresh_book_list()
        self.update_genre_filter()
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="📚 Book Tracker", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # === Форма добавления книги ===
        self.create_input_form(main_frame)
        
        # === Панель фильтрации ===
        self.create_filter_panel(main_frame)
        
        # === Таблица с книгами ===
        self.create_book_table(main_frame)
        
        # === Статус бар ===
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5,0))
    
    def create_input_form(self, parent):
        """Создание формы ввода новой книги"""
        input_frame = ttk.LabelFrame(parent, text="Добавить новую книгу", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Поля ввода
        ttk.Label(input_frame, text="Название книги:*").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.title_entry = ttk.Entry(input_frame, width=35)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Автор:*").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.author_entry = ttk.Entry(input_frame, width=35)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Жанр:*").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.genre_entry = ttk.Entry(input_frame, width=35)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Количество страниц:*").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.pages_entry = ttk.Entry(input_frame, width=35)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопки
        add_btn = ttk.Button(input_frame, text="📖 Добавить книгу", 
                            command=self.add_book)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        delete_btn = ttk.Button(input_frame, text="🗑️ Удалить выбранную книгу", 
                               command=self.delete_book)
        delete_btn.grid(row=2, column=4, columnspan=1, pady=10)
        
        ttk.Label(input_frame, text="* - обязательные поля", 
                 font=('Arial', 8)).grid(row=3, column=0, columnspan=5, sticky=tk.W)
    
    def create_filter_panel(self, parent):
        """Создание панели фильтрации"""
        filter_frame = ttk.LabelFrame(parent, text="Фильтрация книг", padding="10")
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Фильтр по жанру
        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.genre_filter_var = tk.StringVar(value="Все жанры")
        self.genre_filter_combo = ttk.Combobox(filter_frame, textvariable=self.genre_filter_var, 
                                               width=20, state='readonly')
        self.genre_filter_combo.grid(row=0, column=1, padx=5)
        self.genre_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_book_list())
        
        # Фильтр по страницам
        ttk.Label(filter_frame, text="Страниц больше:").grid(row=0, column=2, padx=5)
        self.pages_filter_var = tk.StringVar(value="0")
        self.pages_filter_entry = ttk.Entry(filter_frame, textvariable=self.pages_filter_var, width=10)
        self.pages_filter_entry.grid(row=0, column=3, padx=5)
        
        filter_btn = ttk.Button(filter_frame, text="Применить фильтр", 
                               command=self.refresh_book_list)
        filter_btn.grid(row=0, column=4, padx=10)
        
        reset_btn = ttk.Button(filter_frame, text="Сбросить фильтры", 
                              command=self.reset_filters)
        reset_btn.grid(row=0, column=5, padx=5)
    
    def create_book_table(self, parent):
        """Создание таблицы для отображения книг"""
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Создание Treeview
        columns = ('title', 'author', 'genre', 'pages', 'date_added')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настройка колонок
        self.tree.heading('title', text='Название книги')
        self.tree.heading('author', text='Автор')
        self.tree.heading('genre', text='Жанр')
        self.tree.heading('pages', text='Страницы')
        self.tree.heading('date_added', text='Дата добавления')
        
        self.tree.column('title', width=250)
        self.tree.column('author', width=200)
        self.tree.column('genre', width=120)
        self.tree.column('pages', width=80, anchor=tk.CENTER)
        self.tree.column('date_added', width=150)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def validate_input(self, title: str, author: str, genre: str, pages: str) -> tuple:
        """Валидация вводимых данных"""
        if not title.strip():
            return False, "Название книги не может быть пустым!"
        
        if not author.strip():
            return False, "Автор не может быть пустым!"
        
        if not genre.strip():
            return False, "Жанр не может быть пустым!"
        
        if not pages.strip():
            return False, "Количество страниц не может быть пустым!"
        
        try:
            pages_num = int(pages)
            if pages_num <= 0:
                return False, "Количество страниц должно быть положительным числом!"
            if pages_num > 100000:
                return False, "Количество страниц не может превышать 100000!"
        except ValueError:
            return False, "Количество страниц должно быть целым числом!"
        
        return True, ""
    
    def add_book(self):
        """Добавляет новую книгу"""
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        pages = self.pages_entry.get()
        
        # Валидация
        is_valid, error_msg = self.validate_input(title, author, genre, pages)
        if not is_valid:
            messagebox.showerror("Ошибка ввода", error_msg)
            return
        
        # Добавление книги
        pages_num = int(pages)
        if self.book_manager.add_book(title, author, genre, pages_num):
            messagebox.showinfo("Успех", f"Книга '{title}' успешно добавлена!")
            self.clear_input_fields()
            self.refresh_book_list()
            self.update_genre_filter()
            self.status_var.set(f"Добавлена книга: {title}")
        else:
            messagebox.showwarning("Предупреждение", 
                                  f"Книга '{title}' автора '{author}' уже существует!")
    
    def clear_input_fields(self):
        """Очищает поля ввода"""
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
    
    def refresh_book_list(self):
        """Обновляет список книг с учётом фильтров"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем книги с фильтрацией
        books = self.book_manager.get_books()
        
        # Фильтр по жанру
        selected_genre = self.genre_filter_var.get()
        if selected_genre != "Все жанры":
            books = self.book_manager.filter_by_genre(selected_genre)
        
        # Фильтр по страницам
        try:
            min_pages = int(self.pages_filter_var.get())
            if min_pages > 0:
                books = self.book_manager.filter_by_pages(min_pages - 1)
        except ValueError:
            pass
        
        # Отображаем книги
        for book in books:
            self.tree.insert('', tk.END, values=(
                book.title, book.author, book.genre, 
                book.pages, book.date_added
            ))
        
        count = len(books)
        self.status_var.set(f"Всего книг: {count}")
    
    def delete_book(self):
        """Удаляет выбранную книгу"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите книгу для удаления!")
            return
        
        # Подтверждение удаления
        item = self.tree.item(selected[0])
        book_title = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить книгу '{book_title}'?"):
            # Находим индекс книги
            for i, book in enumerate(self.book_manager.get_books()):
                if book.title == book_title:
                    self.book_manager.remove_book(i)
                    break
            
            self.refresh_book_list()
            self.update_genre_filter()
            self.status_var.set(f"Удалена книга: {book_title}")
    
    def update_genre_filter(self):
        """Обновляет список жанров в фильтре"""
        genres = self.book_manager.get_unique_genres()
        genres.insert(0, "Все жанры")
        self.genre_filter_combo['values'] = genres
        if self.genre_filter_var.get() not in genres:
            self.genre_filter_var.set("Все жанры")
    
    def reset_filters(self):
        """Сбрасывает все фильтры"""
        self.genre_filter_var.set("Все жанры")
        self.pages_filter_var.set("0")
        self.refresh_book_list()
        self.status_var.set("Фильтры сброшены")
