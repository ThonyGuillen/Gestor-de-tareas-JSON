import pytest
from gestor import GestorTareas

gestor = GestorTareas(carpeta='test_tareas')

def test_agregar_tarea():
    gestor.agregar_tarea("Prueba", "Descripcion de prueba", "alta")
    assert len(gestor.tareas) >= 1
