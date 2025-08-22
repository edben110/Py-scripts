import turtle
import json

# Cargar datos del archivo rotado
with open("gengar_contour.json", "r") as f:
    data = json.load(f)

contours = data["contours"]

# Configurar pantalla
screen = turtle.Screen()
screen.bgcolor("black")
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.color("purple")
t.pensize(2)

# Normalizar coordenadas para centrar y escalar
def normalize_coords(coords, scale=1.5, offset_x=0, offset_y=0):
    norm_coords = []
    for x, y in coords:
        norm_x = (x - 180) * scale + offset_x
        norm_y = -(y - 180) * scale + offset_y
        norm_coords.append((norm_x, norm_y))
    return norm_coords

# Dibujar cada contorno
for contour in contours:
    if len(contour) < 2:
        continue
    path = normalize_coords(contour, scale=1.5, offset_x=0, offset_y=-50)
    t.penup()
    t.goto(path[0])
    t.pendown()
    for point in path[1:]:
        t.goto(point)
    t.goto(path[0])  # cerrar el contorno

turtle.done()
