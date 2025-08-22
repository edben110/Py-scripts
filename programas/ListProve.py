lista1 = [2,9,0,8,2,0,0,5]
lista1.sort()
print (lista1)
lista2 = [2,9,0,8,2,0,0,5]
lista3=[]
n=True
if n:
    for n in lista2[:]:
        m = min(lista2)
        lista3.append(m)
       lista2.remove(m)
print(lista2)
print(lista3)