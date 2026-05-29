import sys, os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, conn

@pytest.fixture(autouse=True)
def limpiar_tabla():
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas;")
    conn.commit()
    cur.close()
    yield

@pytest.fixture
def cliente():
    app.testing = True
    return app.test_client()

def test_crear_tarea(cliente):
    res = cliente.post("/tareas", json={"nombre": "Original"})
    assert res.status_code in (200, 201)

    res2 = cliente.get("/")
    assert "Original" in res2.get_data(as_text=True)

def test_editar_tarea_api(cliente):
    cliente.post("/tareas", json={"nombre": "ViejoNombre"})
    cur = conn.cursor()
    cur.execute("SELECT id FROM tareas WHERE nombre = %s;", ("ViejoNombre",))
    tarea_id = cur.fetchone()[0]
    cur.close()

    res_edit = cliente.put(f"/tareas/{tarea_id}", json={"nombre": "NuevoNombre"})
    assert res_edit.status_code == 200
    assert "Tarea editada" in res_edit.get_data(as_text=True)

    res2 = cliente.get("/")
    assert "NuevoNombre" in res2.get_data(as_text=True)
    assert "ViejoNombre" not in res2.get_data(as_text=True)

def test_editar_tarea_form(cliente):
    cliente.post("/tareas", data={"nombre": "ViejoNombre"})
    cur = conn.cursor()
    cur.execute("SELECT id FROM tareas WHERE nombre = %s;", ("ViejoNombre",))
    tarea_id = cur.fetchone()[0]
    cur.close()

    res_edit = cliente.post(f"/tareas/{tarea_id}", data={"_method": "PUT", "nombre": "NuevoNombre"})
    assert res_edit.status_code == 200
    assert "Tarea editada correctamente" in res_edit.get_data(as_text=True)

    res2 = cliente.get("/")
    assert "NuevoNombre" in res2.get_data(as_text=True)
    assert "ViejoNombre" not in res2.get_data(as_text=True)
