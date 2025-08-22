 print('bienvenido al programa de conteo de la palabra mas repetida')

 entrada = "yolo yolo yolo es mi palabra favorita"
 entrada = str(input('ingresa el texto a analizar: '))
 div = entrada.split()
 conteo = {}
 for elemento in div:
    if elemento in conteo:
        conteo[elemento] += 1
    else:
        conteo[elemento] = 1
mas_repetido = max(conteo, key=conteo.get)
 print(f"El objeto más repetido es {mas_repetido}, con {conteo[mas_repetido]} repeticiones.")
print(div)