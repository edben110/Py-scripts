import pandas as pd
import numpy as np

# Semilla para reproducibilidad
np.random.seed(42)

# Localidades y rutas simuladas
localidades = ["Usaquén", "Suba", "Engativá", "Kennedy", "Bosa", "Fontibón",
                "Teusaquillo", "Barrios Unidos", "Chapinero", "Tunjuelito"]

rutas = ["A101", "A102", "B201", "B202", "C301", "C303", "D401", "D404", "E501", "E505"]

# Generar 100 paradas con coordenadas alrededor de Bogotá
paradas = []
for i in range(1, 101):
    loc = np.random.choice(localidades)
    ruta = np.random.choice(rutas)
    
    # Coordenadas centradas en Bogotá (lat ~ 4.6–4.8, lon ~ -74.2 a -74.0)
    lat = np.random.uniform(4.55, 4.80)
    lon = np.random.uniform(-74.20, -74.00)
    
    paradas.append({
        "parada_id": i,
        "nombre_parada": f"Parada_{i}",
        "latitud": lat,
        "longitud": lon,
        "localidad": loc,
        "ruta_alimentador": ruta
    })

df = pd.DataFrame(paradas)
df.to_csv("paradas_alimentador_bogota.csv", index=False)
print("✅ Dataset generado con 100 paradas.")
print(df.head())
