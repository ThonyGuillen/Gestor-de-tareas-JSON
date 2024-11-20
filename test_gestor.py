import pytest
import os
from gestor import GestorTareas, Tarea

@pytest.fixture
def gestor_pruebas():
    # Configura un gestor de tareas para pruebas en un directorio temporal
    gestor = GestorTareas(carpeta='test_tareas')
    # Limpia las tareas previas
    if not os.path.exists('test_tareas'):
        os.makedirs('test_tareas')
    for archivo in os.listdir('test_tareas'):
        os.remove(os.path.join('test_tareas', archivo))
    return gestor

def test_agregar_tarea(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    assert len(gestor_pruebas.tareas) == 1
    assert gestor_pruebas.tareas[0].titulo == "Tarea 1"

def test_listar_tareas(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    tareas = gestor_pruebas.listar_tareas()
    assert len(tareas) == 1
    assert "Tarea 1" in tareas[0]
    assert "Descripción 1" in tareas[0]

def test_completar_tarea(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    resultado = gestor_pruebas.completar_tarea(1)
    assert resultado == "Tarea completada con éxito."
    assert gestor_pruebas.tareas[0].completada is True

def test_eliminar_tarea(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    resultado = gestor_pruebas.eliminar_tarea(1)
    assert resultado == "Tarea eliminada con éxito."
    assert len(gestor_pruebas.tareas) == 0

def test_completar_tarea_indice_invalido(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    resultado = gestor_pruebas.completar_tarea(10)  # Índice inválido
    assert resultado == "Índice de tarea no válido."

def test_eliminar_tarea_indice_invalido(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    resultado = gestor_pruebas.eliminar_tarea(10)  # Índice inválido
    assert resultado == "Índice de tarea no válido."
