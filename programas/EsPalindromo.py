entrada = int(input('Bienvenido al programa adivinador de numero que estas pensando, ingresa un numero del 1 al 9 para calibrar el programa: '))
if entrada:
    print(f'felicidades, el numero que piensas es: {entrada}')
print('bienvenido al programa de deteccion de palindromos')
entrada = str(input('ingresa la palabra a detectar su palindromo: '))
palindromo = False
if entrada == entrada[::-1]:
    print(f'la palabra {entrada} es un palindromo')
    palindromo = True
    print('palindromo: ',palindromo)
else:
    print('palindromo: ',palindromo)