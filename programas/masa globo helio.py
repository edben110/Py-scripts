import math

# Entradas del usuario
circunferencia_globo = float(input('Ingrese la circunferencia total del globo inflado en g: '))
masa_globo_desinflado = float(input('Ingrese la masa experimental total del globo dasinflado en g: '))  # Masa del globo desinflado en gramos
masa_cuerda_experimental = float(input('Ingrese la masa experimental total de la cuerda amarrada al globo inflado en g: '))  # Masa de la cuerda en gramos
distancia = float(input('Ingrese la distancia experimental total entre los globos en cm: '))  # Distancia entre los globos en cm
theta = math.radians(float(input('Ingrese el angulo de inclinacion experimental total del globo: ')))  # Conversión de ángulo a radianes

# Constantes
ke = 9 * (10 ** 9)  # Constante de Coulomb (N·m²/C²)
densidad_aire = 1.225  # Densidad del aire en kg/m³
densidad_elemento_globo = 0.1785  # Densidad del helio en kg/m³
g = 9.81  # Aceleración de la gravedad en m/s²

# Cálculo del radio y volumen del globo
radio_globo = circunferencia_globo / (2 * math.pi)  # Radio del globo en cm
radio_globo_m = radio_globo / 100  # Conversión a metros
volumen_globo = (4/3) * math.pi * (radio_globo_m ** 3)  # Volumen del globo en m³
masa_helio = densidad_elemento_globo * volumen_globo  # Masa de helio en kg
masa_aire = densidad_aire * volumen_globo # Masa del aire desplazado en kg

# Cálculo de fuerzas
fuerza_flotacion = densidad_aire * volumen_globo * g  # Fuerza de flotación en N
peso_globo = ((masa_globo_desinflado / 1000) + masa_helio) * g  # Peso del globo en N
peso_cuerda = fuerza_flotacion - peso_globo  # Peso de la cuerda en N
masa_cuerda = (peso_cuerda / g) * 1000  # Conversión a gramos

# Cálculo de la aceleración del globo
fuerza_empuje = densidad_aire * volumen_globo * g # Fuerza de empuje en N
masa_total = (masa_globo_desinflado / 1000) + masa_helio  # Masa total en kg
fuerza_neta = fuerza_empuje - (masa_total * g)  # Fuerza neta en N
aceleracion_globo = fuerza_neta / masa_total  # Aceleración del globo en m/s²

# Cálculo del error absoluto
error_absoluto = abs(((masa_cuerda - masa_cuerda_experimental) / masa_cuerda) * 100)  # Error porcentual

# Cálculo de la carga eléctrica
peso = (masa_aire + masa_helio + masa_cuerda_experimental) * g  # Peso del globo en N
distancia_m = distancia / 100  # Conversión de distancia a metros
fuerza_electrostatica = (fuerza_empuje - peso) * math.tan(theta)*-1  # Fuerza electrostática derivada del peso y el ángulo pasada a positivo
carga_electrica = math.sqrt((fuerza_electrostatica)*(distancia_m **2)/ ke)*0.01  # Carga experimental en C

# Resultados
print(f"El porcentaje de error es de {error_absoluto:.2f} %")
print(f"La masa de la cuerda es aproximadamente {masa_cuerda:.2f} gramos")
print(f"La fuerza de empuje del globo al ser soltado es aproximadamente {fuerza_empuje:.2f} N")
print(f"La aceleración del globo al ser soltado es aproximadamente {aceleracion_globo:.2f} m/s²")
print(f"La carga eléctrica experimental es de {carga_electrica:.2e} C")
