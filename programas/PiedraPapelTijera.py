import random
print('bienvenido al juego de piedra papel o tijeras ten en cuenta la siguiente tabla')
pc=str(randint(0,2))
tabla=['piedra','papel','tijera']
choice = input('ingresa cualquier valor para jugar: ')
win = True
while win:
    if choice == tabla[int(pc)]:
        print('empate')
        break
    elif choice == 'piedra' and pc =='1':
        win = False
        print('gano papel')
        print('pc escogio papel')
        print('usuario gana:',win)
    elif choice == 'papel' and pc == '2':
        win = False
        print('gano tijeras')
        print('pc escogio tijeras')
        print('usuario gana:',win)
    elif choice == 'tijera' and pc == '0':
        win = False
        print('gano piedra')
        print('pc escogio piedra')
        print('usuario gana:',win)
     else:
        print('pc: ',tabla[int(pc)])
        print('usuario gana:',win)
        break