import json
import os
import sys
from datetime import datetime


def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


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
        return f"{self.titulo} - {self.descripcion} - {self.prioridad} - {self.fecha_creacion} - {estado}"

    @classmethod
    def from_dict(cls, data):
        return cls(
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            prioridad=data["prioridad"],
            fecha_creacion=data.get("fecha_creacion"),
        )


class GestorTareas:
    def __init__(self, carpeta="tareas"):
        self.carpeta = carpeta
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        self.tareas = self.cargar_tareas()

    def agregar_tarea(self, titulo, descripcion, prioridad):
        if prioridad not in ["baja", "media", "alta"]:
            raise ValueError(
                f"Prioridad '{prioridad}' no válida. Use 'baja', 'media' o 'alta'."
            )

        tarea = Tarea(titulo, descripcion, prioridad)
        self.tareas.append(tarea)
        self.guardar_tareas()
        print("Tarea agregada con éxito.")
        self.limpiar_terminal()

    def listar_tareas(self, pausar=True):
        limpiar_pantalla()
        print("\nListado de Tareas")
        print("------------------")
        if not self.tareas:
            print("No hay tareas.")
        for i, tarea in enumerate(self.tareas, 1):
            print(f"{i}. {tarea}")

    def completar_tarea(self, indice, pausar=True):
        try:
            self.tareas[indice - 1].completar()
            self.guardar_tareas()
            return "Tarea completada con éxito."
        except IndexError:
            return "Índice de tarea no válido."
        self.listar_tareas(pausar=pausar)

    def eliminar_tarea(self, indice, pausar=True):
        try:
            tarea_eliminada = self.tareas.pop(indice - 1)
            self.guardar_tareas()
            return "Tarea eliminada con éxito."
        except IndexError:
            return "Índice de tarea no válido."
        self.listar_tareas(pausar=pausar)

    def modificar_tarea(
        self,
        indice,
        nuevo_titulo=None,
        nueva_descripcion=None,
        nueva_prioridad=None,
        pausar=True,
    ):
        if not self.tareas:
            return "No hay tareas para modificar. CREA UNA."

        try:
            tarea = self.tareas[indice - 1]
            if nuevo_titulo:
                tarea.titulo = nuevo_titulo
            if nueva_descripcion:
                tarea.descripcion = nueva_descripcion
            if nueva_prioridad:
                tarea.prioridad = nueva_prioridad
            self.guardar_tareas()
            return "Tarea modificada con éxito."
        except IndexError:
            return "Índice de tarea no válido."
        self.listar_tareas(pausar=pausar)

    def guardar_tareas(self):
        # Eliminar todos los archivos de tareas existentes
        for archivo in os.listdir(self.carpeta):
            if archivo.startswith("Tarea") and archivo.endswith(".json"):
                os.remove(os.path.join(self.carpeta, archivo))

        # Guardar las tareas actuales con nombres actualizados
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
        limpiar_pantalla()


def mostrar_menu(gestor):
    print("\nGestor de Tareas")
    print("----------------")
    print(f"Tareas totales: {gestor.contar_tareas()}")
    print("1. Agregar tarea")
    print("2. Listar tareas")
    print("3. Completar tarea")
    print("4. Eliminar tarea")
    print("5. Modificar tarea")
    print("6. Salir")


def main(args):
    limpiar_pantalla()
    gestor = GestorTareas()

    if args:
        # Procesar argumentos de la línea de comandos
        if args[0] == "agregar":
            # Lógica para agregar una tarea
            pass
        elif args[0] == "listar":
            # Lógica para listar tareas
            pass
        elif args[0] == "completar":
            # Lógica para completar una tarea
            pass
        elif args[0] == "eliminar":
            # Lógica para eliminar una tarea
            pass
        elif args[0] == "modificar":
            # Lógica para modificar una tarea
            pass
        elif args[0] == "salir":
            sys.exit(0)
        else:
            print("Opción no válida")
    else:
        # Modo interactivo
        while True:
            mostrar_menu(gestor)
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                limpiar_pantalla()
                titulo = input("Título de la tarea: ")
                descripcion = input("Descripción de la tarea: ")
                while True:
                    prioridad = input(
                        "Nivel de prioridad (baja, media, alta): "
                    ).lower()
                    if prioridad in ["baja", "media", "alta"]:
                        break
                    else:
                        print(
                            "Prioridad no válida. Por favor, ingrese 'baja', 'media' o 'alta'."
                        )
                gestor.agregar_tarea(titulo, descripcion, prioridad)
            elif opcion == "2":
                gestor.listar_tareas()
            elif opcion == "3":
                try:
                    indice = int(input("Índice de la tarea a completar: "))
                    gestor.completar_tarea(indice)
                except ValueError:
                    limpiar_pantalla()
                    print("Por favor, ingrese un número válido.")
            elif opcion == "4":
                try:
                    indice = int(input("Índice de la tarea a eliminar: "))
                    gestor.eliminar_tarea(indice)
                except ValueError:
                    limpiar_pantalla()
                    print("Por favor, ingrese un número válido.")
            elif opcion == "5":
                if gestor.contar_tareas() == 0:
                    print("No hay tareas para modificar. CREA UNA.")
                    continue
                try:
                    indice = int(input("Índice de la tarea a modificar: "))
                    if indice < 1 or indice > gestor.contar_tareas():
                        limpiar_pantalla()
                        print("Índice de tarea no válido.")
                        continue
                    nuevo_titulo = input(
                        "Nuevo título (dejar en blanco para no modificar): "
                    )
                    nueva_descripcion = input(
                        "Nueva descripción (dejar en blanco para no modificar): "
                    )
                    nueva_prioridad = input(
                        "Nueva prioridad (baja, media, alta) (dejar en blanco para no modificar): "
                    ).lower()
                    if nueva_prioridad and nueva_prioridad not in [
                        "baja",
                        "media",
                        "alta",
                    ]:
                        print(
                            "Prioridad no válida. Por favor, ingrese 'baja', 'media' o 'alta'."
                        )
                        continue
                    gestor.modificar_tarea(
                        indice,
                        nuevo_titulo or None,
                        nueva_descripcion or None,
                        nueva_prioridad or None,
                    )
                except ValueError:
                    print("Por favor, ingrese un número válido.")
                limpiar_pantalla()
            elif opcion == "6":
                print("Saliendo del gestor de tareas. ¡Hasta luego!")
                break
            else:
                limpiar_pantalla()
                print("Opción no válida")


if __name__ == "__main__":
    main(sys.argv[1:])
