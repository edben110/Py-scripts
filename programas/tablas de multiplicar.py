indice=[1,2,3,4,5,6,7,8,9,10]
num_tabla=int(input('ponga el numero de la tabla de multiplicar que desea saber'))
tabla=[]
ind=1
while ind <= 10:
    a = num_tabla * indice[ind]
    tabla.append(a)
    ind += 1
print(indice[1])
    