STATES = {
    "1": "Pendiente",
    "2": "En progreso",
    "3": "Completado"
}

class TaskList:
    def __init__(self):
        self.tasks = []

    def newTask(self, topic):
        task = {"topic": topic, "state": STATES["1"]}  # Por defecto "Pendiente"
        self.tasks.append(task)

    def delTaskByIndex(self, i):
        if 0 <= i < len(self.tasks):
            self.tasks.pop(i)

    def viewList(self):
        return self.tasks

    def updTask(self, i, new_topic):
        if 0 <= i < len(self.tasks):
            self.tasks[i]["topic"] = new_topic

    def updState(self, i, new_state_key):
        if 0 <= i < len(self.tasks) and new_state_key in STATES:
            self.tasks[i]["state"] = STATES[new_state_key]


def table():
    if not task_list.viewList():
        print("No hay tareas registradas.")
        return
    print("\n index | tarea              | estado")
    print("=====================================")
    for i, task in enumerate(task_list.viewList()):
        print(f"  {i:<5} | {task['topic']:<18} | {task['state']}")
    print("=====================================")


# Programa principal
task_list = TaskList()
task_list.newTask("Comprar pan")
task_list.newTask("Comprar leche")

while True:
    print("\n=== Gestor de Tareas ===")
    print("1. Ver tareas")
    print("2. Añadir tarea")
    print("3. Editar tarea")
    print("4. Eliminar tarea")
    print("5. Cambiar estado de tarea")
    print("6. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        table()

    elif opcion == "2":
        topic = input("Escribe la nueva tarea: ")
        if topic.strip():
            task_list.newTask(topic)
            print("Tarea añadida.")
        table()

    elif opcion == "3":
        if not task_list.viewList():
            print("No hay tareas para editar.")
            continue
        table()
        index = input("Número de la tarea a editar: ")
        if index.isdigit():
            index = int(index)
            if 0 <= index < len(task_list.viewList()):
                new_topic = input("Nuevo texto: ")
                task_list.updTask(index, new_topic)
                print("Tarea actualizada.")
            else:
                print("Índice fuera de rango.")
        else:
            print("Debes ingresar un número.")
        table()

    elif opcion == "4":
        if not task_list.viewList():
            print("No hay tareas para eliminar.")
            continue
        table()
        index = input("Número de la tarea a eliminar: ")
        if index.isdigit():
            index = int(index)
            if 0 <= index < len(task_list.viewList()):
                task_list.delTaskByIndex(index)
                print("Tarea eliminada.")
            else:
                print("Índice fuera de rango.")
        else:
            print("Debes ingresar un número.")
        table()

    elif opcion == "5":
        if not task_list.viewList():
            print("No hay tareas para cambiar sus avances.")
            continue
        table()
        index = input("Número de la tarea a cambiar estado: ")
        if index.isdigit():
            index = int(index)
            if 0 <= index < len(task_list.viewList()):
                print("\nEstados disponibles:")
                for k, v in STATES.items():
                    print(f"{k}. {v}")
                opcion_estado = input("Elige un número: ")
                if opcion_estado in STATES:
                    task_list.updState(index, opcion_estado)
                    print("Estado actualizado.")
                else:
                    print("Estado no válido.")
            else:
                print("Índice fuera de rango.")
        else:
            print("Debes ingresar un número.")
        table()

    elif opcion == "6":
        print("Saliendo del gestor de tareas...")
        break

    else:
        print("Opción no válida.")
