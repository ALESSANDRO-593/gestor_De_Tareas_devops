from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="tareas_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# Crear tabla automáticamente si no existe
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);
""")
conn.commit()
cur.close()


@app.route("/")
def home():
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM tareas;")
    tareas = [{"id": row[0], "nombre": row[1]} for row in cur.fetchall()]
    cur.close()
    return render_template("index.html", tareas=tareas)


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    nombre = request.form.get("nombre") or (request.json.get("nombre") if request.json else None)

    if not nombre or nombre.strip() == "":
        if request.form.get("nombre"):
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM tareas;")
            tareas = [{"id": row[0], "nombre": row[1]} for row in cur.fetchall()]
            cur.close()
            return render_template(
                "index.html",
                tareas=tareas,
                error="El nombre de la tarea no puede estar vacío"
            )

        return jsonify({"error": "El nombre de la tarea no puede estar vacío"}), 400

    cur = conn.cursor()
    cur.execute("INSERT INTO tareas (nombre) VALUES (%s);", (nombre,))
    conn.commit()
    cur.close()

    if request.form.get("nombre"):
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM tareas;")
        tareas = [{"id": row[0], "nombre": row[1]} for row in cur.fetchall()]
        cur.close()

        return render_template(
            "index.html",
            tareas=tareas,
            mensaje="Tarea agregada correctamente"
        )

    return jsonify({"mensaje": "Tarea creada"}), 201


@app.route("/tareas/<int:id>", methods=["POST", "PUT"])
def editar_tarea(id):

    # Si vino como POST con _method=PUT
    if request.method == "POST" and request.form.get("_method") == "PUT":
        nuevo_nombre = request.form.get("nombre")
    else:
        nuevo_nombre = request.form.get("nombre") or (
            request.json.get("nombre") if request.json else None
        )

    if not nuevo_nombre or nuevo_nombre.strip() == "":
        if request.form.get("_method"):
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM tareas;")
            tareas = [{"id": row[0], "nombre": row[1]} for row in cur.fetchall()]
            cur.close()

            return render_template(
                "index.html",
                tareas=tareas,
                error="El nombre no puede estar erroneo"
            )

        return jsonify({"error": "El nombre de la tarea no puede estar vacío"}), 400

    cur = conn.cursor()
    cur.execute(
        "UPDATE tareas SET nombre = %s WHERE id = %s;",
        (nuevo_nombre, id)
    )
    conn.commit()
    cur.close()

    if request.form.get("_method"):
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM tareas;")
        tareas = [{"id": row[0], "nombre": row[1]} for row in cur.fetchall()]
        cur.close()

        return render_template(
            "index.html",
            tareas=tareas,
            mensaje="Tarea editada correctamente"
        )

    return jsonify({"mensaje": "Tarea editada"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)