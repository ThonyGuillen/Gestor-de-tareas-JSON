import os
import pytest
from gestor import Tarea, GestorTareas  # Aquí se conecta a gestor.py

@pytest.fixture
def gestor_temporal():
    """Crea un gestor de tareas temporal para pruebas."""
    carpeta = "tareas_prueba"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    gestor = GestorTareas(carpeta=carpeta)
    yield gestor
    # Limpia los archivos generados después de las pruebas
    for archivo in os.listdir(carpeta):
        os.remove(os.path.join(carpeta, archivo))
    os.rmdir(carpeta)

def test_agregar_tarea(gestor_temporal):
    """Prueba agregar una tarea al gestor."""
    gestor_temporal.agregar_tarea("Prueba", "Descripción de prueba", "alta")
    assert len(gestor_temporal.tareas) == 1
    tarea = gestor_temporal.tareas[0]
    assert not tarea.completada

def test_guardar_y_cargar_tareas(gestor_temporal):
    """Prueba que las tareas se guarden y carguen correctamente."""
    gestor_temporal.agregar_tarea("Prueba", "Descripción de prueba", "media")
    gestor_temporal = GestorTareas(carpeta="tareas_prueba")  # Recargar gestor
    assert len(gestor_temporal.tareas) == 1
    tarea = gestor_temporal.tareas[0]
    assert tarea.titulo == "Prueba"
    assert tarea.descripcion == "Descripción de prueba"
    assert tarea.prioridad == "media"
    assert not tarea.completada

def test_completar_tarea(gestor_temporal):
    """Prueba completar una tarea en el gestor."""
    gestor_temporal.agregar_tarea("Prueba", "Descripción de prueba", "baja")
    gestor_temporal.completar_tarea(1, pausar=False)  # Completa la primera tarea sin pausar
    tarea = gestor_temporal.tareas[0]
    assert tarea.completada  # Verifica que la tarea esté completada

def test_eliminar_tarea(gestor_temporal):
    """Prueba eliminar una tarea en el gestor."""
    gestor_temporal.agregar_tarea("Prueba", "Descripción de prueba", "media")
    assert len(gestor_temporal.tareas) == 1
    mensaje = gestor_temporal.eliminar_tarea(1)  # Proporciona el índice directamente
    assert mensaje == "Tarea eliminada con éxito."
    assert len(gestor_temporal.tareas) == 0

def test_modificar_tarea(gestor_temporal):
    """Prueba modificar una tarea en el gestor."""
    gestor_temporal.agregar_tarea("Prueba", "Descripción de prueba", "media")
    mensaje = gestor_temporal.modificar_tarea(
        1,
        nuevo_titulo="Prueba Modificada",
        nueva_descripcion="Descripción modificada",
        nueva_prioridad="alta",
    )
    assert mensaje == "Tarea modificada con éxito."
    tarea = gestor_temporal.tareas[0]
    assert tarea.titulo == "Prueba Modificada"
    assert tarea.descripcion == "Descripción modificada"
    assert tarea.prioridad == "alta"

def test_agregar_con_prioridad_erronea(gestor_temporal):
    """Prueba agregar una tarea con prioridad errónea al gestor."""
    gestor_temporal.agregar_tarea("Prueba", "Descripción de prueba", "masomenos")
    tarea = gestor_temporal.tareas[0]
    assert tarea.titulo == "Prueba"
    assert tarea.descripcion == "Descripción de prueba"
    assert tarea.prioridad == "media"
    assert not tarea.completada