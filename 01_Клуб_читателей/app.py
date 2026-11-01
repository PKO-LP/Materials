import tkinter as tk
from tkinter import ttk, messagebox
import psycopg
from settings import DB
from password_tools import проверить_пароль

второе = None


def вернуться():
    global второе
    if второе is not None:
        второе.destroy()
    второе = None
    окно.deiconify()
    поле.delete(0, tk.END)


def показать_книги():
    if второе is None:
        return
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("SELECT title FROM public.demo_books ORDER BY title")
                записи = курсор.fetchall()
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=второе)
        return
    for строка in таблица.get_children():
        таблица.delete(строка)
    for запись in записи:
        таблица.insert("", tk.END, values=запись)


def войти():
    global второе, таблица
    код = поле.get()  # Одно поле: не нужна отдельная пара логин + пароль.
    if not 1 <= len(код) <= 128:
        messagebox.showwarning("Вход", "Введите учебный код, до 128 символов.", parent=окно)
        return
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("SELECT code_hash FROM public.demo_access WHERE id = 1")
                запись = курсор.fetchone()
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return
    if запись is None or not проверить_пароль(код, запись[0]):
        messagebox.showwarning("Вход", "Код не подходит.", parent=окно)
        return
    поле.delete(0, tk.END)
    второе = tk.Toplevel(окно)
    второе.title("Читательский клуб — список книг")
    второе.geometry("500x310")
    второе.protocol("WM_DELETE_WINDOW", вернуться)
    ttk.Label(второе, text="Книги клуба").pack(pady=8)
    таблица = ttk.Treeview(второе, columns=("title",), show="headings", height=4)
    таблица.heading("title", text="Название")
    таблица.pack(fill="x", padx=15, pady=8)
    ttk.Button(второе, text="Обновить список", command=показать_книги).pack(pady=5)
    ttk.Button(второе, text="Выйти", command=вернуться).pack(pady=5)
    окно.withdraw()
    показать_книги()


окно = tk.Tk()
окно.title("Вход в читательский клуб")
окно.geometry("460x240")
ttk.Label(окно, text="Учебный код доступа").pack(pady=15)
поле = ttk.Entry(окно, width=30, show="*")
поле.pack(pady=5)
кнопка_входа = ttk.Button(окно, text="Войти", command=войти)
кнопка_входа.pack(pady=12)
окно.mainloop()
