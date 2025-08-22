import math
print("Bienvenido al programa de la empresa para calcular el area del terreno")
base = float(input("ponga la base del terreno en mts: "))
altura_triangulo  = float(input("ponga la altura del triangulo en mts: "))
altura_rectangulo = float(input("ponga la altura del rectangulo en mts: "))
area_triangulo = base * altura_triangulo / 2
area_rectangulo = base * altura_rectangulo
area_total = int(area_rectangulo + area_triangulo)
print("el area total del terreno es: ", area_total," mts")

