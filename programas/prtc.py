buscar=input('ingrese la palabra a buscar: ')
palabras = []
def añadirpalabra(palabras):
    palabra = input('ingrese la palabra a agregar: ')
    palabras.append(palabra)
    return palabras
def busqueda(palabras,buscar):
    for buscar in palabras:
        if buscar == buscar:
            return buscar
        return 'no existe palabra'