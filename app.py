
# Importamos las herramientas necesarias de Flask
from flask import Flask, request, jsonify, render_template

# Librería para conectar Python con PostgreSQL
import psycopg2


# Creamos la aplicación Flask
app = Flask(__name__)


# ==============================
# CONEXIÓN A LA BASE DE DATOS
# ==============================

import os

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "tareas_db"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "1234"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432")
)



# ==============================
# CREACIÓN DE TABLA
# ==============================

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente'
);
""")

conn.commit()
cur.close()


# ==============================
# RUTA PRINCIPAL
# ==============================

@app.route("/")
def home():

    cur = conn.cursor()

    cur.execute(
        "SELECT id, nombre, estado FROM tareas;"
    )

    tareas = [
        {
            "id": row[0],
            "nombre": row[1],
            "estado": row[2]
        }
        for row in cur.fetchall()
    ]

    cur.close()

    return render_template(
        "index.html",
        tareas=tareas
    )


# ==============================
# CREAR TAREA
# ==============================

@app.route("/tareas", methods=["POST"])
def crear_tarea():

    nombre = request.form.get("nombre") or (
        request.json.get("nombre")
        if request.json else None
    )

    if not nombre or nombre.strip() == "":

        if request.form.get("nombre"):

            cur = conn.cursor()

            cur.execute(
                "SELECT id, nombre, estado FROM tareas;"
            )

            tareas = [
                {
                    "id": row[0],
                    "nombre": row[1],
                    "estado": row[2]
                }
                for row in cur.fetchall()
            ]

            cur.close()

            return render_template(
                "index.html",
                tareas=tareas,
                error="El nombre de la tarea no puede estar vacío"
            )

        return jsonify({
            "error": "El nombre de la tarea no puede estar vacío"
        }), 400

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tareas (nombre, estado)
        VALUES (%s, 'Pendiente');
        """,
        (nombre,)
    )

    conn.commit()
    cur.close()

    if request.form.get("nombre"):

        cur = conn.cursor()

        cur.execute(
            "SELECT id, nombre, estado FROM tareas;"
        )

        tareas = [
            {
                "id": row[0],
                "nombre": row[1],
                "estado": row[2]
            }
            for row in cur.fetchall()
        ]

        cur.close()

        return render_template(
            "index.html",
            tareas=tareas,
            mensaje="Tarea agregada correctamente"
        )

    return jsonify({"mensaje": "Tarea creada"}), 201


# ==============================
# EDITAR TAREA
# ==============================

@app.route("/tareas/<int:id>", methods=["POST", "PUT"])
def editar_tarea(id):

    if request.method == "POST" and request.form.get("_method") == "PUT":
        nuevo_nombre = request.form.get("nombre")

    else:
        nuevo_nombre = request.form.get("nombre") or (
            request.json.get("nombre")
            if request.json else None
        )

    if not nuevo_nombre or nuevo_nombre.strip() == "":

        if request.form.get("_method"):

            cur = conn.cursor()

            cur.execute(
                "SELECT id, nombre, estado FROM tareas;"
            )

            tareas = [
                {
                    "id": row[0],
                    "nombre": row[1],
                    "estado": row[2]
                }
                for row in cur.fetchall()
            ]

            cur.close()

            return render_template(
                "index.html",
                tareas=tareas,
                error="El nombre no puede estar vacío"
            )

        return jsonify({
            "error": "El nombre de la tarea no puede estar vacío"
        }), 400

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tareas
        SET nombre = %s
        WHERE id = %s;
        """,
        (nuevo_nombre, id)
    )

    conn.commit()
    cur.close()

    if request.form.get("_method"):

        cur = conn.cursor()

        cur.execute(
            "SELECT id, nombre, estado FROM tareas;"
        )

        tareas = [
            {
                "id": row[0],
                "nombre": row[1],
                "estado": row[2]
            }
            for row in cur.fetchall()
        ]

        cur.close()

        return render_template(
            "index.html",
            tareas=tareas,
            mensaje="Tarea editada correctamente"
        )

    return jsonify({"mensaje": "Tarea editada"}), 200


# ==============================
# CAMBIAR ESTADO
# ==============================

@app.route("/tareas/<int:id>/estado", methods=["POST"])
def cambiar_estado(id):

    cur = conn.cursor()

    cur.execute("""
        UPDATE tareas
        SET estado =
            CASE
                WHEN estado = 'Pendiente'
                THEN 'Completada'
                ELSE 'Pendiente'
            END
        WHERE id = %s;
    """, (id,))

    conn.commit()
    cur.close()

    cur = conn.cursor()

    cur.execute(
        "SELECT id, nombre, estado FROM tareas;"
    )

    tareas = [
        {
            "id": row[0],
            "nombre": row[1],
            "estado": row[2]
        }
        for row in cur.fetchall()
    ]

    cur.close()

    return render_template(
        "index.html",
        tareas=tareas,
        mensaje="Estado actualizado correctamente"
    )


# ==============================
# EJECUTAR APLICACIÓN
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )
