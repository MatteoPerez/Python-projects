import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, font
import shutil

def show_custom_messagebox(title, message):
    custom_box = tk.Toplevel()
    custom_box.title(title)
    
    custom_font = font.Font(family="Helvetica", size=24, weight="bold")
    
    message_label = tk.Label(custom_box, text=message, font=custom_font, padx=20, pady=20)
    message_label.pack()

    button_frame = tk.Frame(custom_box)
    button_frame.pack(pady=10)

    yes_button = tk.Button(button_frame, font=custom_font, text="Oui", command=lambda: [custom_box.destroy(), custom_box.yes()])
    yes_button.pack(side="left", padx=10)
    
    no_button = tk.Button(button_frame, font=custom_font, text="Non", command=custom_box.destroy)
    no_button.pack(side="right", padx=10)

    custom_box.yes = lambda: True
    custom_box.no = lambda: False

    custom_box.transient(root)
    custom_box.grab_set()
    root.wait_window(custom_box)

    return custom_box.yes()

def rename_files(all_files):
    new_files_path_list = []

    if not all_files:
        files_names = filedialog.askopenfilenames()
        if not files_names:
            print("Dėmesio - pasirinkite tinkamus failus")
            return
        files_names = list(files_names)
    elif all_files:
        files_directory = filedialog.askdirectory()
        files_names = os.listdir(files_directory)
        files_names = [os.path.join(files_directory, f) for f in files_names]

    for file_path in files_names:
        fileName = os.path.basename(file_path)
        directory = os.path.dirname(file_path)
        position_underscore = fileName.rfind('_')
        position_dot = fileName.rfind('.')
        if position_underscore != -1 and position_dot != -1 and check_file_name(fileName, position_underscore, position_dot):
            number = fileName[position_underscore + 1:position_dot]
            newfilename = number + "_" + fileName[:position_underscore] + fileName[position_dot:]
            new_file_path = os.path.join(directory, newfilename)
            new_files_path_list.append(new_file_path)
            os.rename(file_path, new_file_path)
            print("Naujas failo pavadinimas yra:" + newfilename)
        else:
            print("Atsiprašome, nepavyko pervardyti failo")

    if len(new_files_path_list) == 0:
        return
    move_files = show_custom_messagebox("Perkelti failus", "Ar norėtumėte perkelti pervadintus failus?")
    if move_files:
        dest_folder = filedialog.askdirectory(title="Pasirinkite paskirties aplanką")
        if not dest_folder:
            messagebox.showwarning("Dėmesio", "Pasirinkite tinkamą paskirties aplanką.")
            return
        for file_path in new_files_path_list:
            shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
            print(f"Perkeltas: {file_path} į {dest_folder}")
        print("Geros dienos!")

def check_file_name(fileName, position_underscore, position_dot):
    for i in range(position_underscore + 1, position_dot):
        if not fileName[i].isdigit():
            return False
    return True

root = tk.Tk()
root.title("Pervardyti failus")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Spustelėkite norėdami pasirinkti parinktį")
label.pack(pady=5)

button1 = tk.Button(frame, text="Pasirinkite failą (-us)", command=lambda: rename_files(False))
button1.pack(pady=5)

button2 = tk.Button(frame, text="Pasirinkite visus failus", command=lambda: rename_files(True))
button2.pack(pady=5)

root.mainloop()
