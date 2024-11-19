import tkinter as tk
from tkinter import messagebox
import numpy as np
from collections import OrderedDict

# Расширенная таблица ADFGVX
adfgvx_table = [
    ['p', 'h', '0', 'q', 'g', '6'],
    ['4', 'm', 'e', 'a', '1', 'y'],
    ['l', '2', 'n', 'o', 'f', 'd'],
    ['x', 'k', 'r', '3', 'c', 'v'],
    ['s', '5', 'z', 'w', '7', 'b'],
    ['j', '9', 'u', 't', 'i', '8']
]

# Добавляем недостающие символы
adfgvx_table[5][2] = 'u'  # Добавляем 'u'
adfgvx_table[5][5] = 'b'  # Добавляем 'b'

def adfgvx_encrypt(plaintext, key):
    # Преобразуем текст в последовательность ADFGVX
    adfgvx_text = ''
    for char in plaintext:
        found = False
        for i in range(6):
            for j in range(6):
                if adfgvx_table[i][j] == char:
                    adfgvx_text += 'ADFGVX'[i] + 'ADFGVX'[j]
                    found = True
                    break
            if found:
                break
        if not found:
            messagebox.showwarning("Ошибка", f"Символ '{char}' отсутствует в таблице ADFGVX.")
            return ""

    # Создаем матрицу для шифрования
    key_len = len(key)
    rows = (len(adfgvx_text) + key_len - 1) // key_len
    matrix = np.array([['' for _ in range(key_len)] for _ in range(rows)])

    # Заполняем матрицу
    for i in range(len(adfgvx_text)):
        matrix[i // key_len][i % key_len] = adfgvx_text[i]

    # Сортируем столбцы по ключу
    sorted_key = ''.join(OrderedDict.fromkeys(key))
    sorted_matrix = ['' for _ in range(key_len)]
    for i, char in enumerate(sorted_key):
        col = key.index(char)
        sorted_matrix[i] = ''.join(matrix[:, col])

    # Возвращаем зашифрованный текст
    return ''.join(sorted_matrix)

def adfgvx_decrypt(ciphertext, key):
    # Создаем матрицу для дешифрования
    key_len = len(key)
    rows = (len(ciphertext) + key_len - 1) // key_len
    matrix = np.array([['' for _ in range(key_len)] for _ in range(rows)])

    # Определяем длину каждого столбца
    col_lengths = [rows] * key_len
    for i in range(len(ciphertext) % key_len):
        col_lengths[i] += 1

    # Заполняем матрицу по столбцам
    sorted_key = ''.join(OrderedDict.fromkeys(key))
    index = 0
    for i, char in enumerate(sorted_key):
        col = key.index(char)
        for j in range(col_lengths[i]):
            if index < len(ciphertext):
                matrix[j][col] = ciphertext[index]
                index += 1

    # Восстанавливаем исходный текст
    adfgvx_text = ''.join(matrix.flatten())
    plaintext = ''
    for i in range(0, len(adfgvx_text), 2):
        row = 'ADFGVX'.index(adfgvx_text[i])
        col = 'ADFGVX'.index(adfgvx_text[i + 1])
        plaintext += adfgvx_table[row][col]

    return plaintext

def encrypt_button_click():
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    if plaintext and key:
        ciphertext = adfgvx_encrypt(plaintext, key)
        if ciphertext:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Зашифрованный текст: {ciphertext}")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите текст и ключ.")

def decrypt_button_click():
    ciphertext = ciphertext_entry.get()
    key = key_entry.get()
    if ciphertext and key:
        plaintext = adfgvx_decrypt(ciphertext, key)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Расшифрованный текст: {plaintext}")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите текст и ключ.")

# Создаем главное окно
root = tk.Tk()
root.title("ADFGVX Шифр")

# Создаем и размещаем элементы интерфейса
tk.Label(root, text="Исходный текст:").grid(row=0, column=0, padx=10, pady=10)
plaintext_entry = tk.Entry(root, width=40)
plaintext_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Ключ:").grid(row=1, column=0, padx=10, pady=10)
key_entry = tk.Entry(root, width=40)
key_entry.grid(row=1, column=1, padx=10, pady=10)

encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt_button_click)
encrypt_button.grid(row=2, column=0, padx=10, pady=10)

tk.Label(root, text="Зашифрованный текст:").grid(row=3, column=0, padx=10, pady=10)
ciphertext_entry = tk.Entry(root, width=40)
ciphertext_entry.grid(row=3, column=1, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Расшифровать", command=decrypt_button_click)
decrypt_button.grid(row=4, column=0, padx=10, pady=10)

tk.Label(root, text="Результат:").grid(row=5, column=0, padx=10, pady=10)
result_text = tk.Text(root, height=5, width=40)
result_text.grid(row=5, column=1, padx=10, pady=10)

# Запускаем главный цикл обработки событий
root.mainloop()