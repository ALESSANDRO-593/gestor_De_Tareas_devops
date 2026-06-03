# Importamos las herramientas necesarias de Flask
from flask import Flask, request, jsonify, render_template

# Librería para conectar Python con PostgreSQL
import psycopg2


# Creamos la aplicación Flask
app = Flask(__name__)


# ==============================
# CONEXIÓN A LA BASE DE DATOS
# ==============================

# Conexión con PostgreSQL
conn = psycopg2.connect(
    dbname="tareas_db",     # Nombre de la base de datos
    user="postgres",        # Usuario de PostgreSQL
    password="1234",        # Contraseña
    host="localhost",       # Servidor
    port="5432"             # Puerto de PostgreSQL
)


# ==============================
# CREACIÓN DE TABLA
# ==============================

# Creamos un cursor para ejecutar consultas SQL
cur = conn.cursor()

# Crear la tabla tareas si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,          -- ID automático
    nombre VARCHAR(255) NOT NULL    -- Nombre de la tarea
);
""")

# Guardar cambios en la base de datos
conn.commit()

# Cerrar cursor
cur.close()


# ==============================
# RUTA PRINCIPAL
# ==============================

@app.route("/")
def home():

    # Abrimos cursor
    cur = conn.cursor()

    # Obtener todas las tareas
    cur.execute("SELECT id, nombre FROM tareas;")

    # Convertimos resultados en lista de diccionarios
    tareas = [
        {"id": row[0], "nombre": row[1]}
        for row in cur.fetchall()
    ]

    # Cerramos cursor
    cur.close()

    # Mostrar HTML con las tareas
    return render_template("index.html", tareas=tareas)


# ==============================
# CREAR TAREA
# ==============================

@app.route("/tareas", methods=["POST"])
def crear_tarea():

    # Obtener nombre desde formulario o JSON
    nombre = request.form.get("nombre") or (
        request.json.get("nombre") if request.json else None
    )

    # Validar que no esté vacío
    if not nombre or nombre.strip() == "":

        # Si viene desde formulario HTML
        if request.form.get("nombre"):

            cur = conn.cursor()

            # Obtener tareas actuales
            cur.execute("SELECT id, nombre FROM tareas;")

            tareas = [
                {"id": row[0], "nombre": row[1]}
                for row in cur.fetchall()
            ]

            cur.close()

            # Mostrar error en pantalla
            return render_template(
                "index.html",
                tareas=tareas,
                error="El nombre de la tarea no puede estar vacío"
            )

        # Error en formato JSON
        return jsonify({
            "error": "El nombre de la tarea no puede estar vacío"
        }), 400


    # Insertar nueva tarea en PostgreSQL
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tareas (nombre) VALUES (%s);",
        (nombre,)
    )

    # Guardar cambios
    conn.commit()

    # Cerrar cursor
    cur.close()


    # Si viene desde formulario HTML
    if request.form.get("nombre"):

        cur = conn.cursor()

        cur.execute("SELECT id, nombre FROM tareas;")

        tareas = [
            {"id": row[0], "nombre": row[1]}
            for row in cur.fetchall()
        ]

        cur.close()

        # Mostrar mensaje de éxito
        return render_template(
            "index.html",
            tareas=tareas,
            mensaje="Tarea agregada correctamente"
        )

    # Respuesta JSON
    return jsonify({"mensaje": "Tarea creada"}), 201


# ==============================
# EDITAR TAREA
# ==============================

@app.route("/tareas/<int:id>", methods=["POST", "PUT"])
def editar_tarea(id):

    # Detectar si viene desde formulario HTML
    if request.method == "POST" and request.form.get("_method") == "PUT":
        nuevo_nombre = request.form.get("nombre")

    else:
        # Obtener nombre desde JSON o formulario
        nuevo_nombre = request.form.get("nombre") or (
            request.json.get("nombre") if request.json else None
        )


    # Validar que no esté vacío
    if not nuevo_nombre or nuevo_nombre.strip() == "":

        if request.form.get("_method"):

            cur = conn.cursor()

            cur.execute("SELECT id, nombre FROM tareas;")

            tareas = [
                {"id": row[0], "nombre": row[1]}
                for row in cur.fetchall()
            ]

            cur.close()

            return render_template(
                "index.html",
                tareas=tareas,
                error="El nombre no puede estar erroneo"
            )

        return jsonify({
            "error": "El nombre de la tarea no puede estar vacío"
        }), 400


    # Actualizar tarea en PostgreSQL
    cur = conn.cursor()

    cur.execute(
        "UPDATE tareas SET nombre = %s WHERE id = %s;",
        (nuevo_nombre, id)
    )

    # Guardar cambios
    conn.commit()

    # Cerrar cursor
    cur.close()


    # Si viene desde formulario HTML
    if request.form.get("_method"):

        cur = conn.cursor()

        cur.execute("SELECT id, nombre FROM tareas;")

        tareas = [
            {"id": row[0], "nombre": row[1]}
            for row in cur.fetchall()
        ]

        cur.close()

        return render_template(
            "index.html",
            tareas=tareas,
            mensaje="Tarea editada correctamente"
        )

    # Respuesta JSON
    return jsonify({"mensaje": "Tarea editada"}), 200


# ==============================
# EJECUTAR APLICACIÓN
# ==============================

if __name__ == "__main__":

    # Ejecutar servidor Flask
    app.run(debug=True, port=5000)