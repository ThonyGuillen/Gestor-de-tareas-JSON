import json
import os
from datetime import datetime


class Tarea:
    def __init__(
        self, titulo, descripcion, prioridad, fecha_creacion=None, completada=False
    ):
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fecha_creacion = (
            fecha_creacion
            if fecha_creacion
            else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.completada = completada

    def completar(self):
        self.completada = True

    def __str__(self):
        estado = "Completada" if self.completada else "Pendiente"
        return f"{self.titulo} - {self.descripcion} [Prioridad: {self.prioridad}] [Creada: {self.fecha_creacion}] [{estado}]"

    @classmethod
    def from_dict(cls, data):
        return cls(
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            prioridad=data["prioridad"],
            fecha_creacion=data.get("fecha_creacion"),
            completada=data.get("completada", False),
        )


class GestorTareas:
    def __init__(self, carpeta="tareas"):
        self.carpeta = carpeta
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        self.tareas = self.cargar_tareas()

    def agregar_tarea(self, titulo, descripcion, prioridad):
        tarea = Tarea(titulo, descripcion, prioridad)
        self.tareas.append(tarea)
        self.guardar_tareas()
        print("Tarea agregada con éxito.")
        self.limpiar_terminal()

    def listar_tareas(self):
        print("\nListado de Tareas")
        print("------------------")
        if not self.tareas:
            print("No hay tareas.")
        for i, tarea in enumerate(self.tareas, 1):
            print(f"{i}. {tarea}")
        input("\nPresione Enter para continuar...")
        self.limpiar_terminal()

    def completar_tarea(self, indice):
        try:
            self.tareas[indice - 1].completar()
            self.guardar_tareas()
            print("Tarea completada con éxito.")
        except IndexError:
            print("Índice de tarea no válido.")
        self.listar_tareas()

    def eliminar_tarea(self, indice):
        try:
            tarea = self.tareas.pop(indice - 1)
            self.guardar_tareas()
            print("Tarea eliminada con éxito.")
        except IndexError:
            print("Índice de tarea no válido.")
        self.listar_tareas()

    def guardar_tareas(self):
        for i, tarea in enumerate(self.tareas, 1):
            archivo_tarea = os.path.join(self.carpeta, f"Tarea{i}.json")
            with open(archivo_tarea, "w") as f:
                json.dump(tarea.__dict__, f)

    def cargar_tareas(self):
        tareas = []
        for archivo in sorted(os.listdir(self.carpeta)):
            if archivo.startswith("Tarea") and archivo.endswith(".json"):
                with open(os.path.join(self.carpeta, archivo), "r") as f:
                    data = json.load(f)
                    tareas.append(Tarea.from_dict(data))
        return tareas

    def contar_tareas(self):
        return len(self.tareas)

    def limpiar_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu(gestor):
    print("\nGestor de Tareas")
    print("----------------")
    print(f"Tareas totales: {gestor.contar_tareas()}")
    print("1. Agregar tarea")
    print("2. Listar tareas")
    print("3. Completar tarea")
    print("4. Eliminar tarea")
    print("5. Salir")


def main():
    gestor = GestorTareas()

    while True:
        mostrar_menu(gestor)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            titulo = input("Título de la tarea: ")
            descripcion = input("Descripción de la tarea: ")
            prioridad = input("Nivel de prioridad (baja, media, alta): ")
            gestor.agregar_tarea(titulo, descripcion, prioridad)
        elif opcion == "2":
            gestor.listar_tareas()
        elif opcion == "3":
            indice = int(input("Índice de la tarea a completar: "))
            gestor.completar_tarea(indice)
        elif opcion == "4":
            indice = int(input("Índice de la tarea a eliminar: "))
            gestor.eliminar_tarea(indice)
        elif opcion == "5":
            print("Saliendo del gestor de tareas. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")
            gestor.limpiar_terminal()


if __name__ == "__main__":
    main()
