# Tarea 5 - Formulario de inscripcion para estudiantes

## Objetivo

Crear un formulario donde **nuevos estudiantes se inscriben** a la clase.

Hasta ahora solo mostramos datos. Ahora vamos a **recibir datos** del usuario.

## ¿Por que es importante?

Los formularios son como la "boca" de tu aplicacion web. Los usuarios envian datos (nombre, email) y el servidor los recibe.

## Preparacion

1. Asegurate que Tarea 4 funciona
2. Crea un archivo nuevo: `templates/inscripcion.html`

## Paso 1: Agregar ruta en app.py

Primero, importa `request` de Flask:

```python
from flask import Flask, render_template, request
```

Luego agrega estas funciones:

```python
@app.route("/inscripcion", methods=["GET", "POST"])
def inscripcion():
    mensaje = None
    
    if request.method == "POST":
        # El usuario envio el formulario
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        programa = request.form.get("programa")
        
        # Validacion basica
        if nombre and email and programa:
            mensaje = f"Bienvenido {nombre}! Te hemos registrado."
        else:
            mensaje = "Por favor completa todos los campos."
    
    return render_template("inscripcion.html", mensaje=mensaje)
```

**Explicacion:**
- `methods=["GET", "POST"]` - Acepta GET (ver formulario) y POST (enviar datos)
- `request.form.get("nombre")` - Obtiene el valor del campo "nombre"
- `if request.method == "POST"` - Solo procesa si el usuario envio datos

## Paso 2: Crear el formulario HTML

Crea `templates/inscripcion.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Inscripcion - Portal Clase 1114</title>
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
        </ul>
    </nav>

    <h1>Inscripcion a la Clase</h1>

    <!-- Mostrar mensaje de exito o error -->
    {% if mensaje %}
    <p style="color: green; font-weight: bold;">{{ mensaje }}</p>
    {% endif %}

    <!-- El formulario -->
    <form method="POST">
        <label for="nombre">Nombre:</label>
        <input type="text" name="nombre" id="nombre" required>
        <br><br>

        <label for="email">Email:</label>
        <input type="email" name="email" id="email" required>
        <br><br>

        <label for="programa">Programa:</label>
        <select name="programa" id="programa" required>
            <option value="">-- Selecciona --</option>
            <option value="Sistemas">Sistemas</option>
            <option value="Ingenierias">Ingenierias</option>
            <option value="Otro">Otro</option>
        </select>
        <br><br>

        <button type="submit">Inscribirse</button>
    </form>
</body>
</html>
```

## Paso 3: Actualiza el menu en otras paginas

En todos los `templates/*.html`, agrega al menu:

```html
<li><a href="/inscripcion">Inscripcion</a></li>
```

## Paso 4: Verifica

1. Ve a `http://127.0.0.1:5000/inscripcion`
2. Completa el formulario con nombre, email, programa
3. Haz clic en "Inscribirse"
4. Deberias ver un mensaje de exito

## Paso 5: Prueba validacion

Intenta enviar el formulario **sin llenar un campo**. Deberia rechazarlo (gracias a `required` en HTML).

Intenta enviar sin email valido. HTML no lo permitira (gracias a `type="email"`).

## Conceptos clave

**Formularios HTML:**

```html
<form method="POST">  <!-- Envia datos al servidor -->
    <input name="nombre">  <!-- Campo de texto -->
    <select name="programa">  <!-- Dropdown -->
        <option value="Sistemas">Sistemas</option>
    </select>
    <button type="submit">Enviar</button>  <!-- Boton para enviar -->
</form>
```

**En Python, recibir datos:**

```python
if request.method == "POST":
    nombre = request.form.get("nombre")
    email = request.form.get("email")
```

**Mostrar mensaje en HTML:**

```html
{% if mensaje %}
    <p>{{ mensaje }}</p>
{% endif %}
```

## Preguntas de reflexion

1. ¿Que diferencia hay entre `<input type="text">` y `<input type="email">`?
2. ¿Que hace el atributo `required` en un campo?
3. Si un usuario completa el formulario, ¿donde se guardan esos datos ahora?

## Entregable

Debes mostrar:

1. `app.py` con ruta `/inscripcion` que maneja GET y POST
2. `templates/inscripcion.html` con un formulario completo
3. Menu actualizado en todas las paginas (incluyendo "Inscripcion")
4. Capturas del formulario
5. Captura mostrando el mensaje de exito despues de enviar
6. Captura mostrando validacion (campo vacio rechazado)

## Resumen

Ahora tu portal **recibe datos** de usuarios. 

Pero hay un problema: los datos no se guardan en ningun lado. Si recarga, se pierden.

En la siguiente tarea, vamos a guardar esos datos en una **Base de Datos**.

