"""
Archivo de pruebas unitarias para la aplicación de gestión de tareas.

Estas pruebas verifican:
1. La creación de tareas.
2. La edición de tareas mediante API (PUT).
3. La edición de tareas mediante formularios HTML.

Framework utilizado:
- Pytest
"""

import sys
import os
import pytest

# Agrega la carpeta raíz del proyecto al path
# para poder importar app.py correctamente.
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app import app, conn


@pytest.fixture(autouse=True)
def limpiar_tabla():
    """
    Fixture que se ejecuta automáticamente antes de cada prueba.

    Funciones:
    - Crea la tabla 'tareas' si no existe.
    - Elimina todos los registros para asegurar
      que cada prueba se ejecute en un entorno limpio.
    """

    cur = conn.cursor()

    # Crear tabla si no existe
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    );
    """)

    # Limpiar datos previos
    cur.execute("DELETE FROM tareas;")

    conn.commit()
    cur.close()

    yield


@pytest.fixture
def cliente():
    """
    Crea un cliente de pruebas de Flask.

    Permite realizar solicitudes HTTP simuladas
    sin necesidad de ejecutar el servidor.
    """

    app.testing = True
    return app.test_client()


def test_crear_tarea(cliente):
    """
    Verifica que una tarea pueda crearse correctamente.

    Pasos:
    1. Envía una solicitud POST para crear una tarea.
    2. Comprueba que la respuesta sea exitosa.
    3. Verifica que la tarea aparezca en la página principal.
    """

    res = cliente.post("/tareas", json={"nombre": "Original"})

    assert res.status_code in (200, 201)

    res2 = cliente.get("/")

    assert "Original" in res2.get_data(as_text=True)


def test_editar_tarea_api(cliente):
    """
    Verifica la edición de una tarea mediante la API REST.

    Pasos:
    1. Crear una tarea inicial.
    2. Obtener su ID desde la base de datos.
    3. Editar la tarea mediante PUT.
    4. Verificar que el cambio se haya realizado.
    """

    cliente.post("/tareas", json={"nombre": "ViejoNombre"})

    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM tareas WHERE nombre = %s;",
        ("ViejoNombre",)
    )

    tarea = cur.fetchone()
    tarea_id = tarea[0]

    cur.close()

    res_edit = cliente.put(
        f"/tareas/{tarea_id}",
        json={"nombre": "NuevoNombre"}
    )

    assert res_edit.status_code == 200
    assert "Tarea editada" in res_edit.get_data(as_text=True)

    res2 = cliente.get("/")
    contenido = res2.get_data(as_text=True)

    assert "NuevoNombre" in contenido
    assert "ViejoNombre" not in contenido


def test_editar_tarea_form(cliente):
    """
    Verifica la edición de una tarea utilizando
    un formulario HTML con método POST y override PUT.

    Pasos:
    1. Crear una tarea.
    2. Obtener su ID.
    3. Enviar formulario para editarla.
    4. Confirmar que el nombre fue actualizado.
    """

    cliente.post("/tareas", data={"nombre": "ViejoNombre"})

    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM tareas WHERE nombre = %s;",
        ("ViejoNombre",)
    )

    tarea = cur.fetchone()
    tarea_id = tarea[0]

    cur.close()

    res_edit = cliente.post(
        f"/tareas/{tarea_id}",
        data={
            "_method": "PUT",
            "nombre": "NuevoNombre"
        }
    )

    assert res_edit.status_code == 200
    assert "Tarea editada correctamente" in res_edit.get_data(as_text=True)

    res2 = cliente.get("/")
    contenido = res2.get_data(as_text=True)

    assert "NuevoNombre" in contenido
    assert "ViejoNombre" not in contenido