# Importamos Flask y una funcion que permite mostrar un HTML.
from flask import Flask, render_template, request
from flask import Flask, render_template, request
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key = "1234569"

# Configurar la base de datos
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
    

# Cuando alguien entra a la direccion principal del sitio, Flask ejecuta
# esta funcion y devuelve la pagina `index.html`.
@app.route("/")
def inicio():
    # `render_template` busca archivos dentro de la carpeta `templates`.
    return render_template("index.html")



@app.route("/hola")
def hola():
    # `render_template` busca archivos dentro de la carpeta `templates`.
    return render_template("hola.html")




@app.route("/como")
def como():
    # `render_template` busca archivos dentro de la carpeta `templates`.
    return render_template("como.html")




@app.route("/bien")
def bien():
    # `render_template` busca archivos dentro de la carpeta `templates`.
    return render_template("bien.html")




@app.route("/acerca")
def acerca():
    return render_template("acerca.html")



@app.route("/contacto")
def contacto():
    return render_template("contacto.html")



@app.route("/recursos")
def recursos():
    
    recursos = [
    "Entorno virtual",
    "Rutas en Flask",
    "Plantillas HTML",
    "Variables con Jinja"]

    return render_template("recursos.html"
                           ,recursos=recursos)



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


@app.route("/estudiantes")
def estudiantes():
    # Permitir acceso ÚNICAMENTE al profesor
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    lista_estudiantes = Estudiante.query.all()
    return render_template("estudiantes.html", estudiantes=lista_estudiantes)





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





    


@app.route("/panel-profesor")
def panel_profesor():
    # Verificar que esta logueado y es profesor
    if 'usuario_id' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    return render_template("panel-profesor.html", usuario=session['usuario_nombre'])







@app.route("/panel-estudiante")
def panel_estudiante():
    if 'usuario_id' not in session or session['rol'] != 'estudiante':
        return redirect(url_for("login"))
    
    tareas = Tarea.query.all()
    return render_template("panel_estudiante.html", usuario=session['usuario_nombre'], tareas=tareas)





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
    







    app.route("/crear_tarea", methods=["GET", "POST"])
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








@app.route("/eliminar-tarea/<int:id>")
def eliminar_tarea(id):
    if 'rol' not in session or session['rol'] != 'profesor':
        return redirect(url_for("login"))
    
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    
    return redirect(url_for("mis_tareas"))






 


# Este bloque se ejecuta solo si corremos `python app.py` desde la terminal.
if __name__ == "__main__":
    # `debug=True` sirve en desarrollo porque reinicia el servidor
    # cuando detecta cambios y muestra errores con mas detalle.
    app.run(debug=True)
