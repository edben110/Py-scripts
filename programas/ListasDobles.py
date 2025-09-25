class Nucleotide:
    def __init__(self, base: str):
        self.base = base 
        self.prev = None
        self.next = None


class DNAChain:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, base: str):
        if base == "A":
            pass
        elif base == "T":
            pass
        elif base == "G":
            pass
        elif base == "C":
            pass
        else:
            print("Base inválida. Solo se permiten A, T, G, C.")
            return
        new_node = Nucleotide(base)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove(self, base: str) -> bool:
        current = self.head
        while current:
            if current.base == base:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def show_forward(self):
        current = self.head
        print("Cadena (5' → 3'):")
        while current:
            print(f"[{current.base}]", end=" - ")
            current = current.next
        print("None")

    def show_backward(self):
        current = self.tail
        print("Cadena (3' → 5'):")
        while current:
            print(f"[{current.base}]", end=" - ")
            current = current.prev
        print("None")

dna = DNAChain()
while True:
    print("\n===== MENÚ CADENA DE ADN =====")
    print("1. Agregar nucleótido (A,T,G,C)")
    print("2. Eliminar nucleótido")
    print("3. Mostrar cadena (5' → 3')")
    print("4. Mostrar cadena (3' → 5')")
    print("5. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        valor = input("Ingrese nucleótido: ").upper()
        dna.add(valor)
    elif opcion == "2":
        valor = input("Ingrese nucleótido a eliminar: ").upper()
        if dna.remove(valor):
            print("Nucleótido eliminado.")
        else:
            print("Nucleótido no encontrado.")
    elif opcion == "3":
        dna.show_forward()
    elif opcion == "4":
        dna.show_backward()
    elif opcion == "5":
        print("Saliendo...")
        break
    else:
        print("Opción inválida.")
