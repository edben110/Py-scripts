import serial
import time
from pynput import keyboard

# Configura el puerto COM (ajusta según tu sistema)
ser = serial.Serial('COM3', 115200)  # Cambia COM3 por tu puerto
time.sleep(2)  # Espera a que el ESP32 inicie

pressed_keys = set()

def on_press(key):
    try:
        if key.char:
            pressed_keys.add(key.char.lower())
            if 's' in pressed_keys and 'shift' in pressed_keys:
                print("Comando: medir")
                ser.write(b"medir\n")
    except AttributeError:
        if key == keyboard.Key.shift:
            pressed_keys.add('shift')

def on_release(key):
    try:
        if key.char:
            pressed_keys.discard(key.char.lower())
    except AttributeError:
        if key == keyboard.Key.shift:
            pressed_keys.discard('shift')

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Escuchando teclas... (Shift + S)")
    listener.join()
