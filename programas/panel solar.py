import tkinter as tk
from tkinter import messagebox
import sys

def calcular():
    try:
        prom_consumo_mes = float(entry_consumo.get())
        tarifa_kwh = 900  # COP por kWh

        prom_consumo_dia = prom_consumo_mes / 30
        potencia_necesaria = prom_consumo_dia / 3.9 #hora optima
        cantidad_paneles = potencia_necesaria / 0.55 #Kw por generador
        cantidad_paneles = round(cantidad_paneles) if cantidad_paneles == round(cantidad_paneles) else round(cantidad_paneles) + 1

        # Costos
        costo_panel = 900000
        costo_inversor_y_estructura = 2000000
        costo_instalacion = 1000000
        inversion_total = (cantidad_paneles * costo_panel) + costo_inversor_y_estructura + costo_instalacion

        ahorro_mensual = prom_consumo_mes * tarifa_kwh
        retorno_meses = inversion_total / ahorro_mensual
        retorno_anios = retorno_meses / 12

        # Mostrar resultados
        resultado = (
            f'\nRESULTADOS:\n'
            f'- Consumo diario promedio: {prom_consumo_dia:.2f} kWh\n'
            f'- Potencia requerida: {potencia_necesaria:.2f} kW\n'
            f'- Cantidad de paneles necesarios: {cantidad_paneles} panel(es)\n'
            f'- Inversión total estimada: ${inversion_total:,.0f} COP\n'
            f'- Ahorro mensual aproximado: ${ahorro_mensual:,.0f} COP\n'
            f'- Retorno estimado de inversión: {retorno_meses:.1f} meses ({retorno_anios:.1f} años)'
        )

        text_resultado.config(state='normal')
        text_resultado.delete(1.0, tk.END)
        text_resultado.insert(tk.END, resultado)
        text_resultado.config(state='disabled')

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un valor numérico válido.")

def cerrar():
    ventana.destroy()
    sys.exit()

# Ventana principal
ventana = tk.Tk()
ventana.title("Contador paneles solares")
ventana.geometry("600x400")
ventana.resizable(False, False)

# Manejador de cierre
ventana.protocol("WM_DELETE_WINDOW", cerrar)

# Etiqueta e input
label = tk.Label(ventana, text="Ingrese el promedio de consumo mensual en kWh:", font=("Arial", 12))
label.pack(pady=10)

entry_consumo = tk.Entry(ventana, font=("Arial", 12), width=20, justify="center")
entry_consumo.pack()

# Botón
btn_calcular = tk.Button(ventana, text="Calcular", font=("Arial", 12, "bold"), command=calcular)
btn_calcular.pack(pady=10)

# Área de resultados
text_resultado = tk.Text(ventana, height=12, width=70, font=("Courier New", 10))
text_resultado.pack(pady=10)
text_resultado.config(state='disabled')  # Solo lectura

# Ejecutar
ventana.mainloop()
