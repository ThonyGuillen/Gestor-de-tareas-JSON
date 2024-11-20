import json
import os
from datetime import datetime


class Tarea:
    def __init__(self, titulo, descripcion, prioridad, fecha_creacion=None, completada=False):
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fecha_creacion = (
            fecha_creacion if fecha_creacion else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.completada = completada

    def completar(self):
        self.completada = True

    def __str__(self):
        estado = "Completada" if self.completada else "Pendiente"
        return (
            f"{self.titulo} - {self.descripcion} [Prioridad: {self.prioridad}] "
            f"[Creada: {self.fecha_creacion}] [{estado}]"
        )

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

    def listar_tareas(self):
        return [str(tarea) for tarea in self.tareas]

    def completar_tarea(self, indice):
        try:
            self.tareas[indice - 1].completar()
            self.guardar_tareas()
            return "Tarea completada con éxito."
        except IndexError:
            return "Índice de tarea no válido."

    def eliminar_tarea(self, indice):
        try:
            self.tareas.pop(indice - 1)
            self.guardar_tareas()
            return "Tarea eliminada con éxito."
        except IndexError:
            return "Índice de tarea no válido."

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
    