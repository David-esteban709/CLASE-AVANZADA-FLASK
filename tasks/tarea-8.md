# Tarea 8 - CRUD completo: Crear, editar, eliminar tareas

## Objetivo

Crear un sistema donde el **Profesor** pueda:
- Crear nuevas tareas
- Editar tareas existentes
- Eliminar tareas
- Ver estudiantes inscritos
- Poner calificaciones

Los **Estudiantes** pueden:
- Ver sus tareas asignadas
- Ver calificaciones

## ¿Por que es importante?

CRUD significa Create-Read-Update-Delete. Es el 80% de las aplicaciones web.
Al final de esta tarea, tendras un Portal **completamente funcional**.

## Preparacion

1. Asegurate que Tarea 7 funciona con login
2. Los modelos Usuario y Estudiante ya existen

## Paso 1: Crear modelo Tarea

En `app.py`, agrega:

```python
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_entrega = db.Column(db.Date, nullable=False)
    creada_por = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

    profesor = db.relationship('Usuario', backref='tareas')

    def __repr__(self):
        return f'<Tarea {self.titulo}>'
```

Luego crea la tabla:

```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Tabla Tarea creada")
```

## Paso 2: Crear ruta para crear tarea (Profesor)

```python
@app.route("/crear-tarea", methods=["GET", "POST"])
def crear_tarea():
    # Solo profesor
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        fecha_entrega = request.form.get("fecha_entrega")
        
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha_entrega,
            creada_por=session['usuario_id']
        )
        
        db.session.add(nueva_tarea)
        db.session.commit()
        
        return redirect(url_for("mis_tareas"))
    
    return render_template("crear_tarea.html")

@app.route("/mis-tareas")
def mis_tareas():
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    tareas = Tarea.query.all()
    return render_template("mis_tareas.html", tareas=tareas)
```

## Paso 3: Crear templates/crear_tarea.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear Tarea</title>
</head>
<body>
    <h1>Crear Nueva Tarea</h1>

    <form method="POST">
        <label>Titulo:</label>
        <input type="text" name="titulo" required>
        <br><br>

        <label>Descripcion:</label>
        <textarea name="descripcion" rows="5" required></textarea>
        <br><br>

        <label>Fecha de Entrega:</label>
        <input type="date" name="fecha_entrega" required>
        <br><br>

        <button type="submit">Crear Tarea</button>
        <a href="/mis-tareas"><button type="button">Cancelar</button></a>
    </form>
</body>
</html>
```

## Paso 4: Crear templates/mis_tareas.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mis Tareas</title>
</head>
<body>
    <h1>Mis Tareas</h1>

    <a href="/crear-tarea"><button>Nueva Tarea</button></a>

    {% if tareas %}
    <table border="1">
        <thead>
            <tr>
                <th>Titulo</th>
                <th>Fecha Entrega</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            {% for tarea in tareas %}
            <tr>
                <td>{{ tarea.titulo }}</td>
                <td>{{ tarea.fecha_entrega }}</td>
                <td>
                    <a href="/editar-tarea/{{ tarea.id }}">Editar</a>
                    <a href="/eliminar-tarea/{{ tarea.id }}" onclick="return confirm('¿Eliminar?')">Eliminar</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No hay tareas creadas.</p>
    {% endif %}
</body>
</html>
```

## Paso 5: Ruta para editar tarea

```python
@app.route("/editar-tarea/<int:id>", methods=["GET", "POST"])
def editar_tarea(id):
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    tarea = Tarea.query.get_or_404(id)
    
    if request.method == "POST":
        tarea.titulo = request.form.get("titulo")
        tarea.descripcion = request.form.get("descripcion")
        tarea.fecha_entrega = request.form.get("fecha_entrega")
        
        db.session.commit()
        return redirect(url_for("mis_tareas"))
    
    return render_template("editar_tarea.html", tarea=tarea)
```

## Paso 6: Crear templates/editar_tarea.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Editar Tarea</title>
</head>
<body>
    <h1>Editar Tarea</h1>

    <form method="POST">
        <label>Titulo:</label>
        <input type="text" name="titulo" value="{{ tarea.titulo }}" required>
        <br><br>

        <label>Descripcion:</label>
        <textarea name="descripcion" rows="5" required>{{ tarea.descripcion }}</textarea>
        <br><br>

        <label>Fecha de Entrega:</label>
        <input type="date" name="fecha_entrega" value="{{ tarea.fecha_entrega }}" required>
        <br><br>

        <button type="submit">Guardar Cambios</button>
        <a href="/mis-tareas"><button type="button">Cancelar</button></a>
    </form>
</body>
</html>
```

## Paso 7: Ruta para eliminar tarea

```python
@app.route("/eliminar-tarea/<int:id>")
def eliminar_tarea(id):
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    
    return redirect(url_for("mis_tareas"))
```

## Paso 8: Ver tareas en panel estudiante

En la ruta `panel_estudiante()`:

```python
@app.route("/panel-estudiante")
def panel_estudiante():
    if 'usuario_id' not in session or session['rol'] != 'estudiante':
        return redirect(url_for("login"))
    
    tareas = Tarea.query.all()
    return render_template("panel_estudiante.html", usuario=session['usuario_nombre'], tareas=tareas)
```

Actualiza `templates/panel_estudiante.html`:

```html
<h2>Tus Tareas</h2>

{% if tareas %}
<table border="1">
    <thead>
        <tr>
            <th>Tarea</th>
            <th>Entrega</th>
            <th>Descripcion</th>
        </tr>
    </thead>
    <tbody>
        {% for tarea in tareas %}
        <tr>
            <td>{{ tarea.titulo }}</td>
            <td>{{ tarea.fecha_entrega }}</td>
            <td>{{ tarea.descripcion }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>No hay tareas asignadas.</p>
{% endif %}
```

## Paso 9: Verifica todo

1. Logueate como profesor (henry)
2. Ve a `/crear-tarea`, crea una tarea
3. Ve a `/mis-tareas`, deberia verse la tarea
4. Edita la tarea
5. Logout
6. Logueate como estudiante
7. Ve al panel, deberia ver la tarea creada por el profesor

## Conceptos clave

**CRUD:**
- Create: POST a `/crear-tarea`
- Read: GET `/mis-tareas` muestra tareas
- Update: POST a `/editar-tarea/<id>`
- Delete: GET `/eliminar-tarea/<id>`

**ForeignKey:**

```python
creada_por = db.Column(db.Integer, db.ForeignKey('usuario.id'))
profesor = db.relationship('Usuario', backref='tareas')
```

Conecta Tarea con Usuario. El profesor que creo cada tarea.

**Proteger rutas por rol:**

```python
if session['rol'] != 'profesor':
    return redirect(url_for("login"))
```

## Preguntas de reflexion

1. ¿Que diferencia hay entre Create, Read, Update, Delete?
2. ¿Por que es importante tener ForeignKey entre Tarea y Usuario?
3. ¿Como protegearias la ruta de crear tarea para que solo profesor pueda?

## Entregable

Debes mostrar:

1. `app.py` con modelo Tarea, rutas CRUD
2. `templates/crear_tarea.html`
3. `templates/mis_tareas.html`
4. `templates/editar_tarea.html`
5. Capturas creando una tarea
6. Captura editando una tarea
7. Captura viendo tareas como estudiante
8. Captura eliminando una tarea
9. Captura de la BD mostrando los registros

## FELICIDADES!

Hoy terminaste tu **Portal de Clase completo** con:

✓ Multiples paginas y rutas
✓ Datos dinamicos desde Python
✓ Base de datos SQLite
✓ Autenticacion (Profesor vs Estudiante)
✓ Sistema CRUD (Crear, leer, editar, eliminar)
✓ Permisos por rol

Todo lo que aprendiste en estas 8 tareas es lo que usan **profesionales reales** en aplicaciones web.

Tu portal puede:
- Mostrar informacion de la clase
- Guardar estudiantes inscritos
- Profesor crea y gestiona tareas
- Estudiantes ven sus tareas
- Todo persiste en una BD

**Esto es un proyecto REAL de produccion.**

¿Que sigue?
- Deploy en internet (Heroku, PythonAnywhere)
- Agregar calificaciones
- Sistema de entregas
- Notificaciones por email
- Interfaz visual mejorada

Pero eso ya queda para ustedes. Tienen todas las herramientas. Felicidades!

