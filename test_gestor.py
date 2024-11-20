import pytest
from gestor import Tarea, GestorTareas


# Pruebas para la clase Tarea
def test_crear_tarea():
    tarea = Tarea("Comprar leche", "Ir al supermercado", "alta")
    assert tarea.titulo == "Comprar leche"
    assert tarea.descripcion == "Ir al supermercado"
    assert tarea.prioridad == "alta"
    assert not tarea.completada


def test_completar_tarea():
    tarea = Tarea("Lavar el coche", "Usar jabón especial", "media")
    tarea.completar()
    assert tarea.completada


def test_listar_tareas(capsys, tmpdir):
    gestor = GestorTareas(carpeta=tmpdir)
    gestor.agregar_tarea("Hacer ejercicio", "Gimnasio por 30 minutos", "alta")
    gestor.listar_tareas()
    captured = capsys.readouterr()
    assert "Hacer ejercicio" in captured.out


def test_eliminar_tarea(tmpdir):
    gestor = GestorTareas(carpeta=tmpdir)
    gestor.agregar_tarea("Aprender Python", "Completar tutorial", "media")
    gestor.eliminar_tarea(1)
    assert len(gestor.tareas) == 0


def test_modificar_tarea(tmpdir):
    gestor = GestorTareas(carpeta=tmpdir)
    gestor.agregar_tarea("Correr", "Correr en la cancha de ciclismo", "alta")

    # Modificar tarea
    resultado = gestor.modificar_tarea(
        indice=1,
        nuevo_titulo="Correr rápido",
        nueva_descripcion="Correr en una chanca de ciclismo a gran velocidad",
        nueva_prioridad="media",
    )

    assert resultado == "Tarea modificada con éxito."
    assert gestor.tareas[0].titulo == "Correr rápido"
    assert gestor.tareas[0].descripcion == "Correr en na chanca de ciclismo a  gran velocidad"
    assert gestor.tareas[0].prioridad == "media"

