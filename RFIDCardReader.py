# Attention !! Il faut mettre le clavier en qwerty !!

import keyboard

print("En attente de la carte RFID...")

rfid_data = ""
table = {'0': 0, '1': 1, '2': 2, '3': 3,  
         '4': 4, '5': 5, '6': 6, '7': 7,
         '8': 8, '9': 9, 'a': 10, 'b': 11,
         'c': 12, 'd': 13, 'e': 14, 'f': 15}

def dec(hexadecimal):
    res = 0
    size = len(hexadecimal) - 1
    for num in hexadecimal: 
        res = res + table[num]*16**size 
        size = size - 1
    return res

def handle_rfid(event):
    global rfid_data
    if event.name == 'enter':
        print(f"Card ID : {rfid_data}")
        hex_value = hex(int(rfid_data))
        print(hex_value)
        hex_value = hex_value[4:]
        new_rfid_data = dec(hex_value)
        print(new_rfid_data)
        rfid_data = ""  # Réinitialise la variable pour la prochaine lecture
    else:
        rfid_data += event.name

# Attache la fonction handle_rfid à chaque frappe clavier
keyboard.on_press(handle_rfid)

# Empêche le script de se terminer, en attendant une interruption manuelle
keyboard.wait('esc')  # Appuyez sur 'esc' pour arrêter le programme