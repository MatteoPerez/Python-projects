import keyboard
import tkinter as tk
# import pyperclip  # Biblioteka kopijavimui į atmintį

# Sukuriame pagrindinį tkinter langą
root = tk.Tk()
root.title("RFID 13.56Mhz Skaitytuvas")

# Etiketė, kuri rodys nuskenuotą reikšmę
label = tk.Label(root, text="Laukiama Mifare 13.56Mhz RFID kortelės...", font=("Arial", 14,"bold"))
label.pack(pady=20)
root.geometry("500x300")  # Nustatome lango matmenis

rfid_data = ""
new_rfid_data = ""  # Kintamasis, saugantis nuskenuotą reikšmę

table = {'0': 0, '1': 1, '2': 2, '3': 3,  
         '4': 4, '5': 5, '6': 6, '7': 7,
         '8': 8, '9': 9, 'a': 10, 'b': 11,
         'c': 12, 'd': 13, 'e': 14, 'f': 15}

def dec(hexadecimal):
    res = 0
    size = len(hexadecimal) - 1
    for num in hexadecimal: 
        res = res + table[num] * 16**size 
        size = size - 1
    return res

def decimal_to_two(decimal, bits):
    # Si le nombre est négatif, calculer son complément à 2
    if decimal < 0:
        decimal = (1 << bits) + decimal
    # Convertir le nombre en binaire et remplir avec des zéros pour respecter le nombre de bits
    binaire = format(decimal, f'0{bits}b')
    return binaire

def binary_to_decimal(binaire):
    # Convertir la chaîne binaire en entier en base 10
    decimal = int(binaire, 2)
    return decimal

def convert_to_comma_data(num):
    num = int(num)
    b_num = decimal_to_two(num, 32)
    num1 = binary_to_decimal(b_num[:16])
    num2 = binary_to_decimal(b_num[16:])
    new_num = str(num1) + "," + str(num2)
    return new_num

def binaire_en_decimal(binaire):
    # Convertir la chaîne binaire en entier en base 10
    decimal = int(binaire, 2)
    return decimal

def handle_rfid(event):
    global rfid_data, new_rfid_data
    if event.name == 'enter':
        #label.config(text=label.cget("text") + "\n=============================")
        label.config(text=f"Card ID : {rfid_data}")
        hex_value = hex(int(rfid_data))
        label.config(text=label.cget("text") + f"\nHex : {hex_value}")
        hex_value = hex_value[4:]
        new_rfid_data = dec(hex_value)
        label.config(text=label.cget("text") + f"\nLeidimo numeris : {new_rfid_data}")
        new_rfid_data = convert_to_comma_data(rfid_data)
        label.config(text=label.cget("text") + f"\nAlkortester numeris : {new_rfid_data}")
        rfid_data = ""  # Perkrauname kintamąjį kitam nuskaitymui
    else:
        rfid_data += event.name

# def copy_to_clipboard():
    pyperclip.copy(str(new_rfid_data))
    label.config(text=label.cget("text") + "\n-----------------------------")
    label.config(text=label.cget("text") + f"\nNumeris {new_rfid_data} nukopijuotas į atmintį!")

# Mygtukas, kuris leis nukopijuoti reikšmę
copy_button = tk.Button(root, text="Kopijuoti reikšmę", command=copy_to_clipboard, font=("Arial", 14,"bold"), fg="blue")
copy_button.pack(pady=10)

# Prijungiame funkciją handle_rfid prie kiekvieno klavišo paspaudimo
keyboard.on_press(handle_rfid)

exit_button = tk.Button(root, text="Uzdaryti programa", command=root.destroy,font=("Arial", 14,"bold"), fg="red")#.grid(column=1, row=0)
exit_button.pack(pady=10)

# Paleidžiame tkinter langą
root.mainloop()

# Sulaikome skriptą iki 'esc' paspaudimo
keyboard.wait('esc')  # Paspauskite 'esc' kad sustabdyti programą
