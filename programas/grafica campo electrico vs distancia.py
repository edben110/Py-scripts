import numpy as np
import matplotlib.pyplot as plt

# Constantes 
epsilon_0 = 8.85e-12  
Q = 1
R = 1

# Definición del rango de z
z = np.linspace(0.1, 5, 100)

# Campo eléctrico del anillo en el eje
E_anillo = (Q * z) / (4 * np.pi * epsilon_0 * (R**2 + z**2)**(3/2))

# Densidad de carga superficial del disco
sigma = Q / (np.pi * R**2)

# Campo eléctrico del disco en el eje
E_disco = (sigma / (2 * epsilon_0)) * (1 - z / np.sqrt(R**2 + z**2))

# Graficar los resultados
plt.figure(figsize=(8, 6))
plt.plot(z, E_anillo, label="Anillo", linestyle="--", color="b")
plt.plot(z, E_disco, label="Disco", linestyle="-", color="r")

# Etiquetas y título
plt.xlabel("Distancia (z) [m]")
plt.ylabel("Campo Eléctrico (E) [N/C]")
plt.title("Campo Eléctrico vs Distancia para un Anillo y un Disco")
plt.legend()
plt.grid()
plt.show()