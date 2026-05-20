# Tarea 7 - Autenticacion: Login Profesor vs Estudiante

## Objetivo

Crear un sistema donde **Profesor** y **Estudiantes** se loguean diferente.

- Profesor: acceso especial para crear tareas y calificar
- Estudiante: acceso para ver tareas y calificaciones

## ¿Por que es importante?

No es lo mismo que un estudiante vea TODO. El profesor tiene permisos especiales.
La autenticacion es fundamental en cualquier web moderna.

## Preparacion

1. Asegurate que Tarea 6 funciona con la BD
2. Instala:

```powershell
pip install werkzeug
```

3. Agrega a `requirements.txt`:

```
Flask
flask-sqlalchemy
werkzeug
```

## Paso 1: Agregar modelo Usuario

En `app.py`, antes del modelo Estudiante:

```python
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # "profesor" o "estudiante"

    def establecer_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'
```

**Explicacion:**
- `generate_password_hash()` - Encripta la contraseña
- `check_password_hash()` - Verifica si la contraseña es correcta
- `rol` - Define si es profesor o estudiante

## Paso 2: Importar sesiones

Al inicio de `app.py`:

```python
from flask import Flask, render_template, request, session, redirect, url_for
```

Agrega configuracion de sesion:

```python
app.secret_key = "clave-secreta-super-segura-1114"
```

## Paso 3: Crear BD con usuarios iniciales

En terminal Python:

```python
from app import app, db, Usuario

with app.app_context():
    db.create_all()
    
    # Crear profesor
    if not Usuario.query.filter_by(usuario="henry").first():
        profesor = Usuario(usuario="henry", rol="profesor")
        profesor.establecer_contraseña("password123")
        db.session.add(profesor)
        db.session.commit()
        print("Profesor creado")
```

## Paso 4: Crear ruta de login

En `app.py`:

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = None
    
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        
        user = Usuario.query.filter_by(usuario=usuario).first()
        
        if user and user.verificar_contraseña(contraseña):
            session['usuario_id'] = user.id
            session['usuario_nombre'] = user.usuario
            session['rol'] = user.rol
            
            if user.rol == "profesor":
                return redirect(url_for("panel_profesor"))
            else:
                return redirect(url_for("panel_estudiante"))
        else:
            mensaje = "Usuario o contraseña incorrectos."
    
    return render_template("login.html", mensaje=mensaje)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))
```

## Paso 5: Crear templates/login.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Login - Portal Clase 1114</title>
</head>
<body>
    <h1>Login Portal Clase 1114</h1>
    
    {% if mensaje %}
    <p style="color: red;">{{ mensaje }}</p>
    {% endif %}

    <form method="POST">
        <label>Usuario:</label>
        <input type="text" name="usuario" required>
        <br><br>

        <label>Contraseña:</label>
        <input type="password" name="contraseña" required>
        <br><br>

        <button type="submit">Login</button>
    </form>

    <hr>
    <p>Datos de prueba:</p>
    <p><strong>Profesor:</strong> usuario=henry, contraseña=password123</p>
</body>
</html>
```

## Paso 6: Crear panel del Profesor

```python
@app.route("/panel-profesor")
def panel_profesor():
    # Verificar que esta logueado y es profesor
    if 'usuario_id' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    return render_template("panel_profesor.html", usuario=session['usuario_nombre'])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))
```

## Paso 7: Crear templates/panel_profesor.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel Profesor</title>
</head>
<body>
    <h1>Panel del Profesor</h1>
    <p>Bienvenido, {{ usuario }}</p>

    <nav>
        <ul>
            <li><a href="/">Inicio</a></li>
            <li><a href="/estudiantes">Ver Estudiantes</a></li>
            <li><a href="/logout">Logout</a></li>
        </ul>
    </nav>

    <h2>Acciones del Profesor</h2>
    <ul>
        <li>Crear tareas</li>
        <li>Ver estudiantes inscritos</li>
        <li>Poner calificaciones</li>
    </ul>
</body>
</html>
```

## Paso 8: Crear panel del Estudiante

```python
@app.route("/panel-estudiante")
def panel_estudiante():
    if 'usuario_id' not in session or session['rol'] != 'estudiante':
        return redirect(url_for("login"))
    
    return render_template("panel_estudiante.html", usuario=session['usuario_nombre'])
```

## Paso 9: Crear templates/panel_estudiante.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel Estudiante</title>
</head>
<body>
    <h1>Panel del Estudiante</h1>
    <p>Bienvenido, {{ usuario }}</p>

    <nav>
        <ul>
            <li><a href="/">Inicio</a></li>
            <li><a href="/tareas">Ver Tareas</a></li>
            <li><a href="/logout">Logout</a></li>
        </ul>
    </nav>

    <h2>Tus Tareas</h2>
    <p>Aqui veras las tareas que debes entregar.</p>
</body>
</html>
```

## Paso 10: Proteger rutas

Agrega al inicio de rutas importantes:

```python
@app.route("/estudiantes")
def estudiantes():
    # Permitir acceso a profesor
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    lista_estudiantes = Estudiante.query.all()
    return render_template("estudiantes.html", estudiantes=lista_estudiantes)
```

## Paso 11: Verifica

1. Ve a `/login`
2. Intenta login con usuario=henry, contraseña=password123
3. Deberias ver el panel del profesor
4. Haz click en logout
5. Deberias volver al inicio

## Conceptos clave

**Sesiones:**

```python
session['usuario_id'] = 123  # Guardar en sesion
usuario_id = session.get('usuario_id')  # Leer de sesion
session.clear()  # Limpiar sesion
```

**Contraseñas seguras:**

```python
# No hagas esto
contraseña = "password123"  # NUNCA guardes en texto plano

# Haz esto
hash = generate_password_hash("password123")
db.session.add(usuario)
db.session.commit()

# Verificar
check_password_hash(hash, "password123")  # True
check_password_hash(hash, "malo")  # False
```

**Proteger rutas:**

```python
if 'usuario_id' not in session:
    return redirect(url_for("login"))
```

## Preguntas de reflexion

1. ¿Por que nunca debes guardar contraseñas en texto plano?
2. ¿Que diferencia hay entre crear un Usuario y loguear?
3. ¿Como protegeria la ruta `/estudiantes` para que solo profesor pueda verla?

## Entregable

Debes mostrar:

1. `app.py` con modelos Usuario, rutas login, panel profesor, panel estudiante
2. `templates/login.html` con formulario de login
3. `templates/panel_profesor.html` con menu del profesor
4. `templates/panel_estudiante.html` con menu del estudiante
5. Capturas de login
6. Captura del panel profesor
7. Captura del panel estudiante
8. Captura de logout

## Resumen

Ahora tienes **Autenticacion funcional**. Profesor y Estudiantes ven cosas diferentes.

En la siguiente tarea, vamos a agregar **permisos y CRUD**: crear, leer, editar y eliminar tareas.

