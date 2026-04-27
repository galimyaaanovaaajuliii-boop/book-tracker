"""
Book Tracker - приложение для управления списком прочитанных книг
Автор: Галимьянова Юлия
Версия: 1.0
"""

import tkinter as tk
from gui import BookTrackerGUI

def main():
    """Запуск приложения"""
    try:
        root = tk.Tk()
        app = BookTrackerGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")

if __name__ == "__main__":
    main()
