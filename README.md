# 📋 Gestor de Tareas con Flask y PostgreSQL

Aplicación web sencilla para gestionar tareas, desarrollada con **Flask** y **PostgreSQL**.

El proyecto también incluye:

* ✅ Pruebas automáticas con **Pytest**
* ✅ Integración continua con **GitHub Actions**
* ✅ Configuración básica para CI/CD

---

# 🚀 Tecnologías Utilizadas

* Python
* Flask
* PostgreSQL
* Pytest
* GitHub Actions

---

# 📂 Clonar el Repositorio

```bash
git clone https://github.com/ALESSANDRO-593/gestor_De_Tareas_devops.git
cd gestor_De_Tareas_devops
```
---

# ⚙️ Crear y Activar el Entorno Virtual

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```
---

# 📦 Instalar Dependencias

```bash
pip install -r requirements.txt
```
---

# 🗄️ Configuración de PostgreSQL

Crear la base de datos:

```sql
CREATE DATABASE tareas_db;
```

Seleccionar la base de datos:

```sql
\c tareas_db
```

Crear la tabla de tareas:

```sql
CREATE TABLE tareas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);
```

---

# ▶️ Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en:

👉 http://127.0.0.1:5000

---

# 🧪 Ejecutar las Pruebas

Para ejecutar las pruebas automáticas:

```bash
pytest
```

Si todo funciona correctamente, se mostrará algo similar a:

```bash
3 passed in 0.6s
```

---

# 📌 Funcionalidades

* Crear tareas
* Editar tareas
* Gestión de tareas mediante interfaz web
* Integración con PostgreSQL
* Pruebas automatizadas
* CI/CD con GitHub Actions

---

# 👨‍💻 Autor

Proyecto desarrollado por Alessandro.
