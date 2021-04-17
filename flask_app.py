
import os
import urllib.request
import flask_excel as excel
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functions import allowed_file, get_random_string, verificaEdad

UPLOAD_FOLDER='/home/CristianDeloya/mysite/static/uploads'
FOLDER_CV='/home/CristianDeloya/mysite/static/uploads/cv'
#UPLOAD_FOLDER='static/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'visorcompany2021@gmail.com'
app.config['MAIL_PASSWORD'] = 'domokunsupermami97'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.secret_key = "secret key"
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

@app.route('/')
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        ciudad = request.form['ciudad']
        gusto = request.form['gusto']
        msg = Message('Un usuario dejó sus datos en el portal para ser contactado', sender=("Nuevo contacto para ViSor", "visorcompany2021@gmail.com"), recipients = ["visorcompany2021@gmail.com"])
        msg.html = render_template('emailContact.html', nombre = nombre, correo = correo, telefono = telefono, ciudad = ciudad, gusto = gusto)
        mail.send(msg)
        return render_template('signupSuccess.html')
    else:
	    return render_template('index.html')


@app.route('/opinion', methods=['GET', 'POST'])
def opinion():
	if request.method == 'POST':
		nombre = request.form['nombre']
		correo = request.form['correo']
		telefono = request.form['telefono']
		ciudad = request.form['ciudad']
		gusto = request.form['gusto']
		msg = Message('Un usuario dejó sus datos en el portal para ser contactado', sender=("Nuevo contacto para ViSor", "visorcompany2021@gmail.com"), recipients = ["visorcompany2021@gmail.com"])
		msg.html = render_template('emailContact.html', nombre = nombre, correo = correo, telefono = telefono, ciudad = ciudad, gusto = gusto)
		mail.send(msg)
		return nombre + correo
	else:
		return render_template('opinion.html')


@app.route('/usuarios')
def getUsers():
    users = Usuario.query.all()
    return render_template('dashboard/users.html', users = users)


@app.route('/user/<id>')
def user(id):
    #obtener el usuario de acuerdo al parametro de ID
    user = Usuario.query.get(id)
    if user is None:
        users = Usuario.query.all()
        flash("La información del usuario no se encuentra disponible o no existe")
        return render_template('dashboard/users.html', users = users)
    else:
        return render_template('dashboard/userInfo.html', usuario = user)



#Exportar los datos de la base a un documento Excel
@app.route("/exportar", methods=['GET'])
def exportar():
    query_sets = Usuario.query.all()
    column_names = ['id', 'name','fechaNacimiento', 'edoCivil','ciudad', 'email','telFijo','telCelular','medioEnterado', 'perfil', 'interes', 'expPrevia' ]
    return excel.make_response_from_query_sets(query_sets, column_names, "xls")


#Enviar password temporal para que el usuario tenga acceso a Visor
@app.route("/sendPassword/<id>")
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


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['FOLDER_CV'],
                               filename, as_attachment=True)

@app.route('/deleteUser/<id>')
def delete(id):
	user = Usuario.query.get(id)
	db.session().delete(user)
	db.session().commit()
	flash('Eliminaste un usuario con éxito')
	return redirect(url_for('getUsers'))

@app.route('/login',methods=['GET', 'POST'])
def login():
    return render_template('login.html')

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
	    return render_template('registro.html')

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
    msg.html = render_template('correo.html', value = name)
    mail.send(msg)
    #Save user into database
    fullname = name + ' ' + paterno + ' ' + materno
    user = Usuario(name = fullname, fechaNacimiento = fecha, edoCivil = edoCivil, ciudad = ciudad, email = email, telFijo = fijo, telCelular = celular, nameCV = nameCV, password = randomPassword, tempPassword = 1, medioEnterado = medioEnterado, perfil = perfil, interes = interes, expPrevia = lugarExperiencia)
    db.session.add(user)
    db.session.commit()
    return render_template('signupSuccess.html')

if __name__ == '__main__':
    app.run()





class Usuario(db.Model):

    __tablename__ = "usuarios"

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
    perfil = db.Column(db.String(100))
    interes = db.Column(db.String(100))
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



