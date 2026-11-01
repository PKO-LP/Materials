import tkinter as tk
from tkinter import ttk, messagebox
import psycopg
from settings import DB
from password_tools import создать_хеш, проверить_пароль

второе = None


def зарегистрироваться():
    логин = поле_логина.get().strip()
    пароль = поле_пароля.get()
    if not 3 <= len(логин) <= 30:
        messagebox.showwarning("Проверка", "Логин: 3–30 символов.", parent=окно)
        return
    if not 6 <= len(пароль) <= 128:
        messagebox.showwarning("Проверка", "Пароль: 6–128 символов.", parent=окно)
        return
    хеш = создать_хеш(пароль)  # Готовая функция из соседнего файла.
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("INSERT INTO public.demo_profiles (login, password_hash) VALUES (%s, %s)", (логин, хеш))
    except psycopg.errors.UniqueViolation:
        messagebox.showwarning("Повтор", "Этот логин уже занят.", parent=окно)
        return
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return
    # INSERT уже сохранён при успешном выходе из внешнего with.
    поле_пароля.delete(0, tk.END)
    messagebox.showinfo("Регистрация", "Профиль создан. Введите пароль снова и нажмите «Войти».", parent=окно)


def вернуться():
    global второе
    if второе is not None:
        второе.destroy()
    второе = None
    поле_пароля.delete(0, tk.END)
    окно.deiconify()


def войти():
    global второе
    логин = поле_логина.get().strip()
    пароль = поле_пароля.get()
    if not логин or not пароль:
        messagebox.showwarning("Вход", "Заполните логин и пароль.", parent=окно)
        return
    if len(логин) > 30 or len(пароль) > 128:
        messagebox.showwarning("Вход", "Неверный логин или пароль.", parent=окно)
        return
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("SELECT password_hash FROM public.demo_profiles WHERE login = %s", (логин,))
                запись = курсор.fetchone()
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return
    поле_пароля.delete(0, tk.END)
    if запись is None or not проверить_пароль(пароль, запись[0]):
        messagebox.showwarning("Вход", "Неверный логин или пароль.", parent=окно)
        return
    второе = tk.Toplevel(окно)
    второе.title("Учебный профиль")
    второе.geometry("430x200")
    второе.protocol("WM_DELETE_WINDOW", вернуться)
    ttk.Label(второе, text="Вы вошли как: " + логин).pack(pady=25)
    ttk.Button(второе, text="Вернуться ко входу", command=вернуться).pack(pady=10)
    окно.withdraw()


окно = tk.Tk()
окно.title("Пример: регистрация и вход")
окно.geometry("460x330")
ttk.Label(окно, text="Новый логин: от 3 до 30 символов").pack(pady=8)
поле_логина = ttk.Entry(окно, width=32)
поле_логина.pack(pady=5)
ttk.Label(окно, text="Пароль: от 6 до 128 символов").pack(pady=8)
поле_пароля = ttk.Entry(окно, width=32, show="*")
поле_пароля.pack(pady=5)
кнопка_регистрации = ttk.Button(окно, text="Зарегистрироваться", command=зарегистрироваться)
кнопка_регистрации.pack(pady=8)
кнопка_входа = ttk.Button(окно, text="Войти", command=войти)
кнопка_входа.pack(pady=8)
окно.mainloop()
