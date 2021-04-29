
import os
import urllib.request
import flask_excel as excel

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functions import allowed_file, get_random_string, verificaEdad

#LOGIN
from flask_login import UserMixin
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user

UPLOAD_FOLDER='/home/CristianDeloya/mysite/static/uploads'
FOLDER_CV='/home/CristianDeloya/mysite/static/uploads/cv'
#UPLOAD_FOLDER='static/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = "ingresar"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'visorcompany2021@gmail.com'
app.config['MAIL_PASSWORD'] = 'domokunsupermami97'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.secret_key = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FOLDER_CV'] = FOLDER_CV
app.config['ALLOWED_EXTENSIONS']= ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#Configure database

app.config["DEBUG"] = True
mail = Mail(app)
excel.init_excel(app)

#DATABASE CONFIGURATION
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="CristianDeloya",
    password="Domokun97",
    hostname="CristianDeloya.mysql.pythonanywhere-services.com",
    databasename="CristianDeloya$visor",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)




@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Administrador.query.get(int(user_id))

@app.route('/prueba')
@login_required
def prueba():
    return render_template('dashboard/dashboard.html')

@app.route('/tabla')
@login_required
def tabla():
    return render_template('dashboard/table.html')

@app.route('/ua')
@login_required
def ua():
    return render_template('dashboard/user.html')



#@app.route('/createAdmin')
def createAdmin():
    user = Administrador(name = "Cristian Rosales Deloya", email = "cristiandeloya@gmail.com", password = 'domokunsupermami97')
    db.session.add(user)
    db.session.commit()
    return 'Exito guardando el registro'



@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard/dashboard.html', name=current_user.name)
    else:
        return render_template('landing_page/index.html')

@app.route('/conocenos')
def conocenos():
    return render_template('landing_page/conocenos.html')

@app.route('/perfiles')
def perfiles():
    return render_template('landing_page/perfiles.html')

@app.route('/servicios')
def servicios():
    return render_template('landing_page/servicios.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['email']
        telefono = request.form['telefono']
        ciudad = request.form['ciudad']
        consulta = request.form['consulta']
        msg = Message('Un usuario dejó sus datos en el portal para ser contactado', sender=("Nuevo contacto para ViSor", "visorcompany2021@gmail.com"), recipients = ["visorcompany2021@gmail.com"])
        msg.html = render_template('emailContact.html', nombre = nombre, correo = correo, telefono = telefono, ciudad = ciudad,  consulta = consulta)
        mail.send(msg)
        flash('Tu mensaje fue enviado correctamente, ViSor se pondrá en contacto contigo.')
        return render_template('landing_page/contacto.html')
    else:
        return render_template('landing_page/contacto.html')

@app.route('/ingresar', methods = ['GET', 'POST' ])
def ingresar():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Administrador.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            #Ir a la pantalla de inicio para los administradores
            login_user(user)
            return render_template('dashboard/dashboard.html')
        else:
            #Error al iniciar sesióm
            return render_template('landing_page/login.html')
    else:
        #Solamente se invocó al formulario del login
        return render_template('landing_page/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('landing_page/login.html')

#Login requires

@app.route('/usuarios')
@login_required
def getUsers():
    users = Usuario.query.all()
    return render_template('dashboard/users.html', users = users)

#Select user
@app.route('/user/<id>')
@login_required
def user(id):
    #obtener el usuario de acuerdo al parametro de ID
    user = Usuario.query.get(id)
    if user is None:
        users = Usuario.query.all()
        flash("La información del usuario no se encuentra disponible o no existe")
        return render_template('dashboard/users.html', users = users)
    else:
        return render_template('dashboard/userInfo.html', usuario = user)

#Delete user
@app.route('/deleteUser/<id>')
@login_required
def delete(id):
	user = Usuario.query.get(id)
	db.session().delete(user)
	db.session().commit()
	flash('Eliminaste un usuario con éxito')
	return redirect(url_for('getUsers'))

#Exportar los datos de la base a un documento Excel
@app.route("/exportar", methods=['GET'])
@login_required
def exportar():
    query_sets = Usuario.query.all()
    column_names = ['id', 'name','fechaNacimiento', 'edoCivil','ciudad', 'email','telFijo','telCelular','medioEnterado', 'perfil', 'interes', 'expPrevia' ]
    return excel.make_response_from_query_sets(query_sets, column_names, "xls")


#Enviar password temporal para que el usuario tenga acceso a Visor
@app.route("/sendPassword/<id>")
@login_required
def sendPassword(id):
    usuario = Usuario.query.get(id)
    name = usuario.name
    password =  usuario.password
    email = usuario.email
    #Build mail body and recipients
    msg = Message('Fuiste seleccionad@ para formar parte del equipo de ViSor', sender=("Proyecto ViSor", "visorcompany2021@gmail.com"), recipients = [email])
    msg.html = render_template('dashboard/userSelected.html', name = name, password = password)
    mail.send(msg)
    flash('Has enviado correo electrónico con contraseña temporal exitosamente')
    return redirect(url_for('getUsers'))

#Descargar curriculum
@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['FOLDER_CV'],
                               filename, as_attachment=True)


@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        name = request.form['name']
        paterno = request.form['paterno']
        materno = request.form['materno']
        fecha = request.form['fecha']
        edoCivil = request.form['edoCivil']
        ciudad = request.form['ciudad']
        email = request.form['correo']
        fijo = request.form['fijo']
        celular = request.form['celular']
        medioEnterado = request.form['medioEnterado']
        perfil = request.form['perfil']
        interes = request.form['interes']
        lugarExperiencia = request.form['lugarExperiencia']
        perfil = request.form['perfil']
        file = request.files['cv']

        user = Usuario.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if not verificaEdad(fecha):
            flash('Debes ser mayor de 18 años para poder registrarte en la plataforma.')
            return redirect(url_for('registro'))

        if user:
            flash('La dirección de correo electrónico que ingresaste ya existe.')
            return redirect(url_for('registro'))
    else:
	    return render_template('forms/registro.html')

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
	    filename = secure_filename(file.filename)
	    file.save(os.path.join(app.config['UPLOAD_FOLDER']+"/cv",filename))
	    extension = filename.split(".")
	    extension = str(extension[1])
	    source = UPLOAD_FOLDER+"/cv/"+filename
	    nameCV = name+paterno+materno+"."+extension
	    destination  = UPLOAD_FOLDER+"/cv/"+nameCV
	    os.rename(source,destination)
    else:
	    flash('El archivo que subiste debe estar en formato pdf')
	    return redirect(url_for('registro'))

    #get random password
    randomPassword = get_random_string()

    #Build mail body and recipients
    msg = Message('Detalle de ingreso a la plataforma de ViSor', sender=("Registro existoso ViSor", "visorcompany2021@gmail.com"), recipients = [email])
    msg.html = render_template('emails/correo.html', value = name)
    mail.send(msg)
    #Save user into database
    fullname = name + ' ' + paterno + ' ' + materno
    user = Usuario(name = fullname, fechaNacimiento = fecha, edoCivil = edoCivil, ciudad = ciudad, email = email, telFijo = fijo, telCelular = celular, nameCV = nameCV, password = randomPassword, tempPassword = 1, medioEnterado = medioEnterado, perfil = perfil, interes = interes, expPrevia = lugarExperiencia)
    db.session.add(user)
    db.session.commit()
    return render_template('emails/signupSuccess.html')

@app.route('/registro_opinion', methods = ['GET', 'POST'])
def registro_opinion():
    if request.method == 'POST':
        nombre  = request.form['name']
        paterno = request.form['paterno']
        materno = request.form['materno']
        correo = request.form['correo']
        gusto = request.form['gusto']
        fechaNac = request.form['fecha']
        edoCivil =  request.form['edoCivil']
        return fechaNac
    else:
        return render_template('forms/registroOpinador.html')

@app.route('/admin')
def admin():
    return render_template('baseAdmin.html')

if __name__ == '__main__':
    app.run()



#Models
class Administrador(UserMixin, db.Model):

    __tablename__ = "administrador"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Administrador {}>'.format(self.email)




class Usuario(UserMixin,db.Model):

    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    fechaNacimiento = db.Column(db.String(20))
    edoCivil = db.Column(db.String(20))
    ciudad = db.Column(db.String(50))
    email = db.Column(db.String(100),unique=True)
    telFijo = db.Column(db.String(10))
    telCelular = db.Column(db.String(10))
    nameCV = db.Column(db.String(200))
    password = db.Column(db.String(100))
    tempPassword = db.Column(db.Boolean)
    medioEnterado = db.Column(db.String(100))
    perfil = db.Column(db.String(250))
    expPrevia = db.Column(db.String(500))

    def __init__(self, name, fechaNacimiento, edoCivil, ciudad, email, telFijo, telCelular, nameCV, password, tempPassword, medioEnterado, perfil,interes,  expPrevia):
        self.name = name
        self.fechaNacimiento = fechaNacimiento
        self.edoCivil = edoCivil
        self.ciudad = ciudad
        self.email = email
        self.telFijo = telFijo
        self.telCelular = telCelular
        self.nameCV = nameCV
        self.password = password
        self.tempPassword = tempPassword
        self.medioEnterado = medioEnterado
        self.perfil = perfil
        self.interes = interes
        self.expPrevia = expPrevia

    def __repr__(self):
        return '<User {}>'.format(self.name)



