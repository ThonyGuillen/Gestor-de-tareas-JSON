import pytest
import os
from gestor import GestorTareas, Tarea

@pytest.fixture
def gestor_pruebas():
    # Configura un gestor de tareas para pruebas en un directorio temporal
    gestor = GestorTareas(carpeta='test_tareas')
    # Limpia las tareas previas
    for archivo in os.listdir('test_tareas'):
        os.remove(os.path.join('test_tareas', archivo))
    return gestor

def test_agregar_tarea(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    assert len(gestor_pruebas.tareas) == 1
    assert gestor_pruebas.tareas[0].titulo == "Tarea 1"

def test_listar_tareas(gestor_pruebas, capsys):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    gestor_pruebas.listar_tareas()
    captured = capsys.readouterr()
    assert "Tarea 1" in captured.out
    assert "Descripción 1" in captured.out

def test_completar_tarea(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    gestor_pruebas.completar_tarea(1)
    assert gestor_pruebas.tareas[0].completada is True

def test_eliminar_tarea(gestor_pruebas):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    gestor_pruebas.eliminar_tarea(1)
    assert len(gestor_pruebas.tareas) == 0

def test_completar_tarea_indice_invalido(gestor_pruebas, capsys):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    gestor_pruebas.completar_tarea(10)  # Índice inválido
    captured = capsys.readouterr()
    assert "Índice de tarea no válido" in captured.out

def test_eliminar_tarea_indice_invalido(gestor_pruebas, capsys):
    gestor_pruebas.agregar_tarea("Tarea 1", "Descripción 1", "alta")
    gestor_pruebas.eliminar_tarea(10)  # Índice inválido
    captured = capsys.readouterr()
    assert "Índice de tarea no válido" in captured.out
