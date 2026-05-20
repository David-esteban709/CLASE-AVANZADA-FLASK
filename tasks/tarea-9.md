# Tarea 9 - Diseño Profesional: CSS y Bootstrap

## Objetivo

Transformar el Portal de Clase de HTML plano a una **aplicacion web visualmente profesional** usando Bootstrap.

Hasta ahora se enfocaron en lógica y funcionalidad. Ahora vamos a hacer que **se vea bien**.

## ¿Por que es importante?

Una aplicacion web sin diseño se ve amateur. Bootstrap permite hacer interfaces profesionales sin ser un diseñador.

Los usuarios juzgan por lo que ven. La funcionalidad sin diseño es invisible.

## Preparacion

1. Asegurate que las Tareas 1-8 funcionan completamente
2. Abre `templates/index.html`

## Paso 1: Agregar Bootstrap al index.html

En la etiqueta `<head>`, agrega Bootstrap CDN:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Clase 1114</title>
    
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <style>
        body {
            background-color: #f8f9fa;
        }
        
        .navbar {
            background-color: #667eea;
        }
        
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            margin-bottom: 40px;
        }
        
        .hero h1 {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        .card {
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        
        .footer {
            background-color: #343a40;
            color: white;
            padding: 20px 0;
            margin-top: 40px;
            text-align: center;
        }
    </style>
</head>
<body>
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Clase 1114</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Inicio</a></li>
                    <li class="nav-item"><a class="nav-link" href="/informacion">Informacion</a></li>
                    <li class="nav-item"><a class="nav-link" href="/recursos">Recursos</a></li>
                    <li class="nav-item"><a class="nav-link" href="/tareas">Tareas</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inscripcion">Inscripcion</a></li>
                    {% if session.get('usuario_id') %}
                    <li class="nav-item"><a class="nav-link" href="/logout">Logout</a></li>
                    {% else %}
                    <li class="nav-item"><a class="nav-link" href="/login">Login</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <div class="hero">
        <div class="container">
            <h1>Bienvenidos a Clase 1114</h1>
            <p class="lead">Introduccion a Python y Flask</p>
        </div>
    </div>

    <!-- CONTENIDO PRINCIPAL -->
    <div class="container my-5">
        <div class="row">
            <div class="col-md-6">
                <h2>Informacion de la Clase</h2>
                <p><strong>Profesor:</strong> {{ profesor }}</p>
                <p><strong>Email:</strong> {{ email }}</p>
                <p><strong>Horario:</strong> {{ horario }}</p>
                <p><strong>Aula:</strong> {{ aula }}</p>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Descripcion</h5>
                        <p class="card-text">{{ descripcion }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- CARDS DESTACADAS -->
    <div class="container my-5">
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Tareas</h5>
                        <p class="card-text">Ver todas las tareas entregables del curso.</p>
                        <a href="/tareas" class="btn btn-primary">Ver Tareas</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Recursos</h5>
                        <p class="card-text">Documentacion y enlaces educativos.</p>
                        <a href="/recursos" class="btn btn-primary">Ver Recursos</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Inscripcion</h5>
                        <p class="card-text">Registrate como estudiante de la clase.</p>
                        <a href="/inscripcion" class="btn btn-primary">Inscribirse</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Portal Clase 1114 | Profesor: Henry Ortegon | Kyrbot Innovations</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Paso 2: Actualizar informacion.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informacion - Clase 1114</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .navbar { background-color: #667eea; }
        .footer { background-color: #343a40; color: white; padding: 20px 0; margin-top: 40px; text-align: center; }
    </style>
</head>
<body>
    <!-- NAVBAR (igual para todas las paginas) -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Clase 1114</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Inicio</a></li>
                    <li class="nav-item"><a class="nav-link" href="/informacion">Informacion</a></li>
                    <li class="nav-item"><a class="nav-link" href="/recursos">Recursos</a></li>
                    <li class="nav-item"><a class="nav-link" href="/tareas">Tareas</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inscripcion">Inscripcion</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- CONTENIDO -->
    <div class="container my-5">
        <h1 class="mb-4">Informacion de la Clase</h1>
        
        <div class="row mb-4">
            <div class="col-md-6">
                <h3>Detalles</h3>
                <ul class="list-group">
                    <li class="list-group-item"><strong>Aula:</strong> {{ aula }}</li>
                    <li class="list-group-item"><strong>Profesor:</strong> {{ profesor }}</li>
                    <li class="list-group-item"><strong>Horario:</strong> {{ horario }}</li>
                </ul>
            </div>
            <div class="col-md-6">
                <h3>Objetivos</h3>
                <ul class="list-group">
                    {% for objetivo in objetivos %}
                    <li class="list-group-item">{{ objetivo }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Portal Clase 1114</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Paso 3: Crear archivo base.html (Template herencia)

Para evitar repetir navbar y footer, crea `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Portal Clase 1114{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .navbar { background-color: #667eea; }
        body { background-color: #f8f9fa; }
        .footer { background-color: #343a40; color: white; padding: 20px 0; margin-top: 40px; text-align: center; }
    </style>
</head>
<body>
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Clase 1114</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Inicio</a></li>
                    <li class="nav-item"><a class="nav-link" href="/informacion">Informacion</a></li>
                    <li class="nav-item"><a class="nav-link" href="/recursos">Recursos</a></li>
                    <li class="nav-item"><a class="nav-link" href="/tareas">Tareas</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inscripcion">Inscripcion</a></li>
                    {% if session.get('usuario_id') %}
                    <li class="nav-item"><a class="nav-link" href="/logout">Logout</a></li>
                    {% else %}
                    <li class="nav-item"><a class="nav-link" href="/login">Login</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- CONTENIDO DE LA PAGINA -->
    <main class="container my-5">
        {% block content %}{% endblock %}
    </main>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Portal Clase 1114 | Profesor: Henry Ortegon | Kyrbot Innovations</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Paso 4: Usar base.html en otras plantillas

Cambia `templates/tareas.html`:

```html
{% extends "base.html" %}

{% block title %}Tareas - Clase 1114{% endblock %}

{% block content %}
<h1 class="mb-4">Tareas Entregables</h1>

{% if tareas %}
<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>Numero</th>
            <th>Titulo</th>
            <th>Fecha entrega</th>
        </tr>
    </thead>
    <tbody>
        {% for tarea in tareas %}
        <tr>
            <td>{{ tarea.numero }}</td>
            <td>{{ tarea.titulo }}</td>
            <td>{{ tarea.fecha }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p class="alert alert-info">No hay tareas aun.</p>
{% endif %}
{% endblock %}
```

## Paso 5: Actualizar formularios

`templates/inscripcion.html`:

```html
{% extends "base.html" %}

{% block title %}Inscripcion - Clase 1114{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <h1 class="mb-4">Inscripcion a la Clase</h1>

        {% if mensaje %}
        <div class="alert alert-success">{{ mensaje }}</div>
        {% endif %}

        <form method="POST" class="needs-validation">
            <div class="mb-3">
                <label for="nombre" class="form-label">Nombre:</label>
                <input type="text" class="form-control" name="nombre" id="nombre" required>
            </div>

            <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" class="form-control" name="email" id="email" required>
            </div>

            <div class="mb-3">
                <label for="programa" class="form-label">Programa:</label>
                <select name="programa" class="form-select" id="programa" required>
                    <option value="">-- Selecciona --</option>
                    <option value="Sistemas">Sistemas</option>
                    <option value="Ingenierias">Ingenierias</option>
                    <option value="Otro">Otro</option>
                </select>
            </div>

            <button type="submit" class="btn btn-primary w-100">Inscribirse</button>
        </form>
    </div>
</div>
{% endblock %}
```

## Conceptos clave

**Bootstrap:** Framework CSS que proporciona componentes listos.

```html
<!-- Boton -->
<button class="btn btn-primary">Boton</button>

<!-- Card -->
<div class="card">
    <div class="card-body">Contenido</div>
</div>

<!-- Tabla -->
<table class="table table-striped">...</table>
```

**Template Herencia en Jinja2:**

```html
<!-- base.html -->
{% block content %}{% endblock %}

<!-- otra.html -->
{% extends "base.html" %}
{% block content %}Mi contenido{% endblock %}
```

Esto evita repetir navbar y footer en cada pagina.

## Preguntas de reflexion

1. ¿Que ventaja tiene usar Bootstrap vs escribir CSS manualmente?
2. ¿Como ayuda template herencia a mantener el codigo limpio?
3. ¿Que otras mejoras visuales podrias hacer?

## Entregable

Debes mostrar:

1. `base.html` con navbar, footer, estilos Bootstrap
2. `index.html` con hero section y cards
3. Minimo 3 templates actualizados con Bootstrap
4. Todas las paginas con navbar y footer consistentes
5. Formularios con estilos Bootstrap
6. Tablas con estilos mejorados
7. Capturas de cada pagina mostrando el nuevo diseño

## Resumen

Tu Portal ahora **se ve profesional**. Aprendiste:
- Bootstrap para diseño rapido
- Template herencia para reutilizar codigo
- CSS basico para personalizar
- Responsive design (adapta a movil)

**Felicitaciones!** Completaste todas las tareas del curso.

Ahora tienes un **Portal Web COMPLETO y PROFESIONAL** que:
✓ Funciona correctamente
✓ Se ve bien visualmente
✓ Es responsive (funciona en movil)
✓ Tiene autenticacion
✓ Tiene CRUD
✓ Usa base de datos
✓ Sigue buenas practicas

Esto es un proyecto **REAL** de produccion. Felicidades!

