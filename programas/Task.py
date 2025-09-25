from datetime import datetime

class Task:
    def __init__(self, topic, description, state, priority, category,
                 assigned_to, progress, due_date, tags, visibility, difficulty):
        self.topic = topic
        self.description = description
        self.state = self.set_state(state)
        self.priority = self.set_priority(priority)
        self.category = self.set_category(category)
        self.assigned_to = assigned_to
        self.progress = progress
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.due_date = due_date
        self.tags = tags
        self.visibility = self.set_visibility(visibility)
        self.difficulty = self.set_difficulty(difficulty)
        self.next = None

    def set_state(self, key):
        if key == "1": return "Pendiente"
        elif key == "2": return "En progreso"
        elif key == "3": return "Completado"
        else: return "Pendiente"

    def set_priority(self, key):
        if key == "1": return "Baja"
        elif key == "2": return "Media"
        elif key == "3": return "Alta"
        else: return "Media"

    def set_category(self, key):
        if key == "1": return "Personal"
        elif key == "2": return "Trabajo"
        elif key == "3": return "Estudio"
        else: return "Personal"

    def set_visibility(self, key):
        if key == "1": return "Pública"
        elif key == "2": return "Privada"
        else: return "Pública"

    def set_difficulty(self, key):
        if key == "1": return "Fácil"
        elif key == "2": return "Media"
        elif key == "3": return "Difícil"
        else: return "Media"

class TaskList:
    def __init__(self):
        self.head = None 

    def newTask(self, topic, description="", state="1", priority="2", category="1",
                assigned_to="", progress=0, due_date="", tags="", visibility="1", difficulty="2"):
        new_node = Task(topic, description, state, priority, category,
                        assigned_to, progress, due_date, tags, visibility, difficulty)  
        if not self.head: 
            self.head = new_node
        else: 
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def getTask(self, index):
        current = self.head
        i = 0
        while current:
            if i == index:
                return current
            current = current.next
            i += 1
        return None

    def updState(self, index, new_state_key):
        task = self.getTask(index)
        if task:
            task.state = task.set_state(new_state_key)
            return True
        return False

    def isEmpty(self):
        return self.head is None


def table():
    if task_list.isEmpty():
        print("No hay tareas registradas.")
        return
    print("\n   #   | tarea        | estado       | prioridad | categoría | dificultad | visibilidad | prog% | fecha límite | asignado a | etiquetas | descripción")
    print("===========================================================================================================================================")
    current = task_list.head
    i = 0
    while current:
        print(f"  {i:<5} | {current.topic:<12} | {current.state:<12} | {current.priority:<9} | {current.category:<9} | {current.difficulty:<10} | {current.visibility:<11} | {current.progress:<5} | {current.due_date:<12} | {current.assigned_to:<10} | {current.tags:<9} | {current.description}")
        current = current.next
        i += 1
    print("===========================================================================================================================================")

task_list = TaskList()
task_list.newTask("Comprar pan", "Ir a la panadería", priority="3", category="1", difficulty="1", visibility="2")
task_list.newTask("Proyecto", "Entregar informe final", state="2", priority="3", category="2", assigned_to="Equipo", progress=50, due_date="2025-09-25", tags="importante", difficulty="3")

while True:
    print("\n=== Gestor de Tareas ===")
    print("1. Ver tareas")
    print("2. Añadir tarea")
    print("3. Cambiar estado de tarea")
    print("4. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        table()

    elif opcion == "2":
        topic = input("Escribe la nueva tarea: ")
        description = input("Añade una descripción: ")
        print("Prioridad: 1. Baja  2. Media  3. Alta")
        priority = input("Elige un número: ")
        print("Categoría: 1. Personal  2. Trabajo  3. Estudio")
        category = input("Elige un número: ")
        print("Visibilidad: 1. Pública  2. Privada")
        visibility = input("Elige un número: ")
        print("Dificultad: 1. Fácil  2. Media  3. Difícil")
        difficulty = input("Elige un número: ")
        due_date = input("Fecha límite (YYYY-MM-DD): ")
        assigned_to = input("Asignado a: ")
        tags = input("Etiquetas: ")
        if topic.strip():
            task_list.newTask(topic, description, "1", priority, category, assigned_to, 0, due_date, tags, visibility, difficulty)
            print("Tarea añadida.")
        table()

    elif opcion == "3":
        table()
        index = input("Número de la tarea a cambiar estado: ")
        if index.isdigit():
            print("Estados: 1. Pendiente  2. En progreso  3. Completado")
            opcion_estado = input("Elige un número: ")
            if task_list.updState(int(index), opcion_estado):
                print("Estado actualizado.")
            else:
                print("Estado no válido o índice fuera de rango.")
        table()

    elif opcion == "4":
        print("Saliendo del gestor de tareas...")
        break

    else:
        print("Opción no válida.")
