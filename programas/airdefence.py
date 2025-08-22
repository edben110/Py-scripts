import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
import ipywidgets as widgets

# Función para calcular la posición del misil en función del tiempo
def calcular_trayectoria(v0, theta, t, x0=0, direccion_derecha=True):
    g = 9.81  # Gravedad en m/s^2
    theta_rad = np.radians(theta)  # Convertir ángulo a radianes
    
    # Si el misil va hacia la izquierda, invertir el signo de la componente horizontal
    direccion = 1 if direccion_derecha else -1
    x = x0 + direccion * v0 * np.cos(theta_rad) * t
    y = v0 * np.sin(theta_rad) * t - 0.5 * g * t**2
    return x, y

# Función para encontrar el tiempo de vuelo máximo
def tiempo_vuelo_max(v0, theta):
    g = 9.81
    theta_rad = np.radians(theta)
    return (2 * v0 * np.sin(theta_rad)) / g

# Función para calcular el tiempo de intersección
def calcular_interseccion(v0_1, theta_1, v0_2, theta_2, x0_aa):
    t_interseccion = np.linspace(0, min(tiempo_vuelo_max(v0_1, theta_1), tiempo_vuelo_max(v0_2, theta_2)), 1000)
    for t in t_interseccion:
        x1, y1 = calcular_trayectoria(v0_1, theta_1, t)
        x2, y2 = calcular_trayectoria(v0_2, theta_2, t, x0=x0_aa, direccion_derecha=False)  # Misil AA a la izquierda
        if np.isclose(x1, x2, atol=1) and np.isclose(y1, y2, atol=1):
            return t, x1, y1
    return None, None, None

# Función para graficar las trayectorias y punto de intersección
def graficar_trayectorias(v0_1, theta_1, v0_2, theta_2, x0_aa):
    # Crear un vector de tiempo para cada misil
    t1 = np.linspace(0, tiempo_vuelo_max(v0_1, theta_1), 500)
    t2 = np.linspace(0, tiempo_vuelo_max(v0_2, theta_2), 500)
    
    # Calcular trayectorias
    x1, y1 = calcular_trayectoria(v0_1, theta_1, t1)
    x2, y2 = calcular_trayectoria(v0_2, theta_2, t2, x0=x0_aa, direccion_derecha=False)  # Misil AA hacia la izquierda
    
    # Graficar trayectorias
    plt.figure(figsize=(10, 5))
    plt.plot(x1, y1, label="Misil balístico", color="blue")
    plt.plot(x2, y2, label="Misil antiaéreo", color="red")

    # Calcular intersección
    t_interseccion, x_interseccion, y_interseccion = calcular_interseccion(v0_1, theta_1, v0_2, theta_2, x0_aa)
    
    if t_interseccion is not None:
        plt.scatter(x_interseccion, y_interseccion, color="green", zorder=5)
        plt.text(x_interseccion, y_interseccion, f"Intersección: ({x_interseccion:.2f}, {y_interseccion:.2f})", fontsize=12)
    else:
        plt.text(0.5, 0.5, "No hay intersección", fontsize=12, transform=plt.gca().transAxes, color="green")
    
    # Configuraciones del gráfico
    plt.title("Trayectorias del misil balístico y misil antiaéreo")
    plt.xlabel("Distancia (m)")
    plt.ylabel("Altura (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Crear los sliders para velocidad y ángulo de cada misil
vo_misilBLT = FloatSlider(
    min=0, 
    max=200, 
    step=1, 
    value=100, 
    description="V Misil blt (m/s)"
    )
theta_misilBLT = FloatSlider(min=0, max=90, step=1, value=45, description="Áng Misil blt (°)")

vo_misilAA = FloatSlider(
    min=0, 
    max=200, 
    step=1, 
    value=100, 
    description="V Misil AA (m/s)"
    )
theta_misilAA= FloatSlider(
    min=0, 
    max=90, 
    step=1, 
    value=45, 
    description="Áng Misil AA (°)"
    )

# Slider para la posición de disparo del misil antiaéreo
x0_misilAA = FloatSlider(
    min=50, 
    max=1000, 
    step=10, 
    value=1000, 
    description="Posición Misil AA (m)"
    )

# Usar interact para crear la interfaz gráfica
interact(graficar_trayectorias, 
         v0_1=vo_misilBLT, 
         theta_1=theta_misilBLT, 
         v0_2=vo_misilAA, 
         theta_2=theta_misilAA,
         x0_aa=x0_misilAA);
