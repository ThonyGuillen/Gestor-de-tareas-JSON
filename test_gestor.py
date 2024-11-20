import pytest
from gestor import GestorTareas

def test_agregar_tarea():
    gestor = GestorTareas(carpeta='test_tareas')
    gestor.agregar_tarea("Prueba", "Descripción de prueba", "alta")
    assert len(gestor.tareas) == 1
