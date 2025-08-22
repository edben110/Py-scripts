from random import randint

iniciador = True
adivinador=randint(0,20)
print(adivinador)
oportunidades = 5
print('bienvenido a el juego de adivina el numero, tienes 5 oportunidades')
def numero():
    entrada=int(input('por favor ingresa un numero del 1 al 20: '))
    return entrada
while iniciador:
    if oportunidades > 0:
        entrada = numero()
        if entrada == adivinador:
            print('has ganado')
            iniciador=False
        elif entrada < adivinador:
            oportunidades -= 1
            print(f'el numero a adivinar es mayor que {entrada}, tienes {oportunidades} oportunidades')
        elif entrada > adivinador:
            oportunidades -= 1
            print(f'el numero a adivinar es menor que {entrada}, tienes {oportunidades} oportunidades')
    else:
        print('has perdido')
        iniciador=False