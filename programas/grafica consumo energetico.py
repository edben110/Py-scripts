import matplotlib.pyplot as plt

# Meses del año
meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Lista para almacenar los consumos
consumos = []

# Ingreso de datos
print("Ingrese el consumo energético (kWh) de cada mes:")

for mes in meses:
    while True:
        try:
            consumo = float(input(f"{mes}: "))
            consumos.append(consumo)
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")

# Graficar
plt.figure(figsize=(10, 6))
plt.bar(meses, consumos, color='skyblue')
plt.title("Consumo Energético Mensual del Hogar (kWh)")
plt.xlabel("Meses")
plt.ylabel("Consumo (kWh)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
