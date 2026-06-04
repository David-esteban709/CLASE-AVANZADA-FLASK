from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "1234569"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    programa = db.Column(db.String(50), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Estudiante {self.nombre}>'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    def establecer_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_entrega = db.Column(db.Date, nullable=False)
    creada_por = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    # AGREGADA: Esta columna permitirá guardar la nota del alumno
    calificacion = db.Column(db.Float, nullable=True) 

    profesor = db.relationship('Usuario', backref='tareas')

    def __repr__(self):
        return f'<Tarea {self.titulo}>'

@app.route('/')
def inicio():
    # Aquí definimos la info de la clase
    info_clase = {
        "profesor": "Henry Ortegon",
        "github": "henryor",
        "horario": "Lunes a Viernes - 07:00 AM",
        "aula": "Laboratorio de Sistemas 1114"
    }
    return render_template('index.html', info=info_clase)

@app.route("/hola")
def hola():
    return render_template("hola.html")

@app.route("/como")
def como():
    return render_template("como.html")

@app.route("/bien")
def bien():
    return render_template("bien.html")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/recursos")
def recursos():
    recursos_lista = [
        "Entorno virtual",
        "Rutas en Flask",
        "Plantillas HTML",
        "Variables con Jinja"
    ]
    return render_template("recursos.html", recursos=recursos_lista)

@app.route("/informacion")
def informacion():
    aula_clase = "Sala de Sistemas / Sección 1114"
    nombre_profesor = "Profesor Henry"
    horario_clase = "Miercoles y Jueves"
    objetivos_lista = [
        "Comprender la arquitectura Cliente-Servidor usando Flask.",
        "Aprender a diseñar bases de datos relacionales con SQLAlchemy.",
        "Implementar sistemas de autenticación y control de roles (Profesor/Estudiante).",
        "Estilizar interfaces web profesionales e interactivas con Bootstrap."
    ]
    return render_template("informacion.html", aula=aula_clase, profesor=nombre_profesor, horario=horario_clase, objetivos=objetivos_lista)

@app.route("/inscripcion", methods=["GET", "POST"])
def inscripcion():
    mensaje = None
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        programa = request.form.get("programa")
        
        if not nombre or not email or not programa:
            mensaje = "Por favor completa todos los campos."
        else:
            try:
                nuevo_estudiante = Estudiante(
                    nombre=nombre,
                    email=email,
                    programa=programa
                )
                db.session.add(nuevo_estudiante)
                db.session.commit()
                mensaje = f"¡Bienvenido {nombre}! Te hemos registrado."
            except Exception as e:
                db.session.rollback()
                mensaje = "Error: Este email ya está registrado."
    
    return render_template("inscripcion.html", mensaje=mensaje)

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

from flask import session, redirect, url_for

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

@app.route("/panel_profesor")
def panel_profesor():
    if 'usuario_id' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
        
    return render_template("panel_profesor.html", usuario=session.get('usuario_nombre'))

@app.route("/panel_estudiante")
def panel_estudiante():
    if 'usuario_id' not in session or session['rol'] != 'estudiante':
        return redirect(url_for("login"))
        
    tareas = Tarea.query.all()
    return render_template("panel_estudiante.html", usuario=session.get('usuario_nombre'), tareas=tareas)


@app.route("/tareas")
def tareas():
    lista_tareas = Tarea.query.all()
    return render_template("mis_tareas.html", tareas=lista_tareas)

@app.route("/estudiantes")
def estudiantes():
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    lista_estudiantes = Estudiante.query.all()
    return render_template("estudiantes.html", estudiantes=lista_estudiantes)

@app.route("/crear-tarea", methods=["GET", "POST"])
def crear_tarea():
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        fecha_texto = request.form.get("fecha_entrega")
        
        fecha_objeto = datetime.strptime(fecha_texto, '%Y-%m-%d').date()
        
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha_objeto,
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
    

@app.route("/editar-tarea/<int:id>", methods=["GET", "POST"])
def editar_tarea(id):
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    tarea = Tarea.query.get_or_404(id)
    
    if request.method == "POST":
        tarea.titulo = request.form.get("titulo")
        tarea.descripcion = request.form.get("descripcion")
        fecha_texto = request.form.get("fecha_entrega")
        
        # AQUÍ ESTÁ LO QUE FALTABA:
        tarea.calificacion = request.form.get("calificacion") 
        
        tarea.fecha_entrega = datetime.strptime(fecha_texto, '%Y-%m-%d').date()
        
        
        db.session.commit() # ¡Esto guarda los cambios!
        return redirect(url_for("mis_tareas"))
    


    if request.method == "POST":
        tarea.titulo = request.form.get("titulo")
        tarea.descripcion = request.form.get("descripcion")
        tarea.calificacion = request.form.get("calificacion") 
        
        # Validación de seguridad: solo convertimos si recibimos una fecha
        fecha_texto = request.form.get("fecha_entrega")
        if fecha_texto:
            tarea.fecha_entrega = datetime.strptime(fecha_texto, '%Y-%m-%d').date()
        
        db.session.commit()
        return redirect(url_for("mis_tareas"))
    

    
    
    return render_template("editar_tarea.html", tarea=tarea)
  
    


@app.route("/eliminar-tarea/<int:id>")
def eliminar_tarea(id):
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    
    return redirect(url_for("mis_tareas"))

if __name__ == "__main__":
    app.run(debug=True)