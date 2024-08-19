import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

def rename_files(all_files):
    new_files_path_list = []
    
    if(all_files == False):
        files_names = filedialog.askopenfilenames()
        if not files_names:
            print(("Dėmesio - pasirinkite tinkamus failus")) # Attention - Please select valid files
            return
        files_names = list(files_names)
    elif(all_files == True):
        files_directory = filedialog.askdirectory()
        files_names = os.listdir(files_directory)
        files_names = [os.path.join(files_directory, f) for f in files_names]
    
    for file_path in files_names:
        fileName = os.path.basename(file_path)
        directory = os.path.dirname(file_path)
        position_underscore = fileName.rfind('_')
        position_dot = fileName.rfind('.')
        if position_underscore != -1 and position_dot != -1 and check_file_name(fileName, position_underscore, position_dot) == True:
            # print("_ = " + str(position_underscore) + "   " + fileName)
            # print(". = " + str(position_dot) + "   " + fileName)
            number = fileName[position_underscore + 1:position_dot]
            newfilename = number + "_" + fileName[:position_underscore] + fileName[position_dot:]
            new_file_path = os.path.join(directory, newfilename)
            new_files_path_list.append(new_file_path)
            os.rename(file_path, new_file_path)
            print("Naujas failo pavadinimas yra:" + newfilename) # New file name is : 
        else:
            print("Atsiprašome, nepavyko pervardyti failo") # Sorry, couldn't rename file
    
    if len(new_files_path_list) == 0:
        return
    move_files = messagebox.askyesno("Perkelti failus", "Ar norėtumėte perkelti pervadintus failus?") # "Move files", "Would you like to move renamed files ?"
    if move_files:
        dest_folder = filedialog.askdirectory(title="Pasirinkite paskirties aplanką") # Select destination folder
        if not dest_folder:
            messagebox.showwarning("Dėmesio", "pasirinkite tinkamą paskirties aplanką.") # "Attention", "please select a valid destination folder."
            return
        for file_path in new_files_path_list:
            shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
            print(f"Perkeltas: {file_path} į {dest_folder}") # Moved : {file_path} to {dest_folder}
        print("Geros dienos!") # Have a good day!

def check_file_name(fileName, position_underscore, position_dot):
    for i in range(position_underscore+1,position_dot):
            if fileName[i].isdigit() == False:
                return False
    return True

root = tk.Tk()
root.title("Pervardyti failus") #

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Spustelėkite norėdami pasirinkti parinktį") # Click to select option
label.pack(pady=5)

button1 = tk.Button(frame, text="Pasirinkite failą (-us)", command=lambda:rename_files(False)) # Select file(s)
button1.pack(pady=5)

button2 = tk.Button(frame, text="Pasirinkite visus failus", command= lambda:rename_files(True)) # Select all files
button2.pack(pady=5)

root.mainloop()