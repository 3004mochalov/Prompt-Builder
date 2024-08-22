import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os

def select_files():
    global selected_files_label
    file_paths = filedialog.askopenfilenames()
    filenames_to_display = []
    for file_path in file_paths:
        filenames_to_display.append(os.path.basename(file_path))  # Append the filename first.

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except UnicodeDecodeError:
            prompt_text.insert(tk.END, f'{os.path.basename(file_path)}\n\n')
            continue

        prompt_text.insert(tk.END, f'вот файл {os.path.basename(file_path)}:\n\n{file_content}\n\n')

    selected_files_label.config(text="Открытые файлы: " + ", ".join(filenames_to_display))

def reset_prompt():
    # Очистка данных без сохранения
    prompt_text.delete('1.0', tk.END)
    selected_files_label.config(text="Открытые файлы: ")  # Сбросить метку выбранных файлов

def save_prompt():
    prompt = prompt_text.get('1.0', tk.END)
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_path = os.path.join(os.getcwd(), 'saved')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f'prompt_{current_datetime}.txt')
    with open(file_path, 'w') as file:
        file.write(prompt)

    # Очистка данных после сохранения
    prompt_text.delete('1.0', tk.END)
    selected_files_label.config(text="Открытые файлы: ")  # Сбросить метку выбранных файлов


def open_prompt():
    folder_path = os.path.join(os.getcwd(), 'saved')
    if os.path.exists(folder_path):
        os.startfile(folder_path)

def paste_from_clipboard(event=None):
    try:
        text = root.clipboard_get()
        prompt_text.insert(tk.INSERT, text)
    except tk.TclError:
        pass  # Если ничего нет в буфере обмена, ничего не делаем

root = tk.Tk()
root.geometry("1280x960")
root.title('Prompt Builder')

# Привязываем горячую клавишу Ctrl+V (или Command+V на MacOS) к функции paste_from_clipboard
root.bind('<Control-v>', paste_from_clipboard)  # Или замените '<Control-v>' на '<Command-v>' для MacOS

frame = tk.Frame(root)
frame.pack(pady=10)

select_button = tk.Button(frame, text='Выбрать файлы', command=select_files)
select_button.grid(row=0, column=0)

save_button = tk.Button(frame, text='Сохранить промпт', command=save_prompt)
save_button.grid(row=0, column=1)

open_button = tk.Button(frame, text='Открыть промпты', command=open_prompt)
open_button.grid(row=0, column=2)

reset_button = tk.Button(frame, text='Сбросить изменения', command=reset_prompt)
reset_button.grid(row=0, column=3)

# Добавляем метку для отображения выбранных файлов
selected_files_label = tk.Label(root, text="Открытые файлы: ", anchor='w')
selected_files_label.pack(fill='both')

prompt_text = tk.Text(root, height=20, width=50)
prompt_text.pack(pady=10, expand=True, fill='both')

# Создаем полосу прокрутки
scrollbar = tk.Scrollbar(root, command=prompt_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Располагаем полосу прокрутки справа

# Настраиваем Text виджет на использование полосы прокрутки
prompt_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
