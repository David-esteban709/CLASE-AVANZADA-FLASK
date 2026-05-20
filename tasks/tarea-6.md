# Tarea 6 - Base de datos: Guardar inscritos con SQLAlchemy

## Objetivo

Guardar los datos de inscripcion en una **Base de Datos SQLite**.

Hasta ahora los datos se perdian al recargar. Ahora van a **persistir** (quedarse guardados).

## ¿Por que es importante?

Una aplicacion web real necesita guardar datos. Un portal sin BD no sirve para nada.

Usaremos **SQLAlchemy**, que es un ORM (Object-Relational Mapping) que facilita trabajar con bases de datos.

## Preparacion

1. Asegurate que Tarea 5 funciona
2. Instala dependencias nuevas:

```powershell
pip install flask-sqlalchemy
```

3. Agrega al `requirements.txt`:

```
Flask
flask-sqlalchemy
```

Luego:
```powershell
pip install -r requirements.txt
```

## Paso 1: Configurar la BD en app.py

Al inicio de `app.py`, agrega:

```python
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

## Paso 2: Crear modelo de Estudiante

Antes de las rutas, define el modelo:

```python
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    programa = db.Column(db.String(50), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Estudiante {self.nombre}>'
```

**Explicacion:**
- `id` - Identificador unico de cada estudiante
- `nombre`, `email`, `programa` - Campos del formulario
- `nullable=False` - El campo es obligatorio
- `unique=True` - No puede haber dos estudiantes con el mismo email
- `fecha_inscripcion` - Fecha automatica

## Paso 3: Crear la tabla en la BD

Abre una terminal Python en la carpeta del proyecto:

```powershell
python
```

Luego:

```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Base de datos creada!")
```

Escribe `exit()` para salir.

Deberia haber un archivo nuevo: `portal.db`

## Paso 4: Modificar la ruta de inscripcion

Reemplaza la funcion `inscripcion()` en `app.py`:

```python
@app.route("/inscripcion", methods=["GET", "POST"])
def inscripcion():
    mensaje = None
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        programa = request.form.get("programa")
        
        # Validacion
        if not nombre or not email or not programa:
            mensaje = "Por favor completa todos los campos."
        else:
            try:
                # Crear nuevo estudiante
                nuevo_estudiante = Estudiante(
                    nombre=nombre,
                    email=email,
                    programa=programa
                )
                
                # Guardar en BD
                db.session.add(nuevo_estudiante)
                db.session.commit()
                
                mensaje = f"Bienvenido {nombre}! Te hemos registrado."
            except Exception as e:
                db.session.rollback()
                mensaje = f"Error: Este email ya esta registrado."
    
    return render_template("inscripcion.html", mensaje=mensaje)
```

## Paso 5: Agregar pagina de estudiantes

Crea una ruta para ver todos los inscritos:

```python
@app.route("/estudiantes")
def estudiantes():
    lista_estudiantes = Estudiante.query.all()
    return render_template("estudiantes.html", estudiantes=lista_estudiantes)
```

## Paso 6: Crear templates/estudiantes.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estudiantes - Portal Clase 1114</title>
</head>
<body>
    <!-- MENU -->
    <nav>
        <ul>
            <li><a href="/">Inicio</a></li>
            <li><a href="/informacion">Informacion</a></li>
            <li><a href="/recursos">Recursos</a></li>
            <li><a href="/tareas">Tareas</a></li>
            <li><a href="/inscripcion">Inscripcion</a></li>
            <li><a href="/estudiantes">Estudiantes</a></li>
        </ul>
    </nav>

    <h1>Estudiantes Inscritos ({{ estudiantes|length }})</h1>

    {% if estudiantes %}
    <table border="1">
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Email</th>
                <th>Programa</th>
                <th>Fecha Inscripcion</th>
            </tr>
        </thead>
        <tbody>
            {% for estudiante in estudiantes %}
            <tr>
                <td>{{ estudiante.nombre }}</td>
                <td>{{ estudiante.email }}</td>
                <td>{{ estudiante.programa }}</td>
                <td>{{ estudiante.fecha_inscripcion.strftime('%d/%m/%Y %H:%M') }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No hay estudiantes inscritos aun.</p>
    {% endif %}
</body>
</html>
```

## Paso 7: Verifica

1. Abre `http://127.0.0.1:5000/inscripcion`
2. Inscribe a 3 estudiantes diferentes
3. Abre `http://127.0.0.1:5000/estudiantes`
4. Deberias ver una tabla con los estudiantes guardados
5. Recarga la pagina. **Los datos persisten!**

Eso es el poder de una BD: los datos quedan guardados.

## Conceptos clave

**Modelos SQLAlchemy:**

```python
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
```

**Guardar datos:**

```python
nuevo = Estudiante(nombre="Ana", email="ana@mail.com")
db.session.add(nuevo)
db.session.commit()
```

**Leer datos:**

```python
todos = Estudiante.query.all()  # Todos
uno = Estudiante.query.filter_by(nombre="Ana").first()  # Un resultado
```

## Preguntas de reflexion

1. ¿Que es un ORM y por que simplifica trabajar con bases de datos?
2. ¿Que diferencia hay entre `db.session.add()` y `db.session.commit()`?
3. ¿Por que `unique=True` es importante en el email?

## Entregable

Debes mostrar:

1. `app.py` con modelo `Estudiante` y BD configurada
2. `requirements.txt` con `flask-sqlalchemy`
3. `templates/estudiantes.html` mostrando tabla de inscritos
4. Archivo `portal.db` en la carpeta del proyecto
5. Capturas inscribiendo 3 estudiantes
6. Captura de la pagina `/estudiantes` mostrando los 3 inscritos
7. Captura despues de recargar, mostrando que los datos persisten

## Resumen

Ahora tienes una **Base de Datos funcional**. Los datos se guardan y persisten.

En la siguiente tarea, vamos a agregar **Autenticacion**: Profesor y Estudiantes tendran login diferentes.

