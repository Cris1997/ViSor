
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from functions import allowed_file, get_random_string

UPLOAD_FOLDER='/home/CristianDeloya/mysite/static/uploads'
#UPLOAD_FOLDER='static/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'trabajoterminal2019a085@gmail.com'
app.config['MAIL_PASSWORD'] = 'domokunsupermami97'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#Configure database

app.config["DEBUG"] = True

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
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		#flash("Password must be at least 10 characters")
	else:
		return render_template('login.html')

@app.route('/opinion', methods=['GET', 'POST'])
def opinion():
	if request.method == 'POST':
		nombre = request.form['nombre']
		correo = request.form['correo']
		telefono = request.form['telefono']
		ciudad = request.form['ciudad']
		gusto = request.form['gusto']
		msg = Message('Un usuario dejó sus datos en el portal para ser contactado', sender=("Nuevo contacto para ViSor", "trabajoterminal2019a085@gmail.com"), recipients = ["trabajoterminal2019a085@gmail.com"])
		msg.html = render_template('emailContact.html', nombre = nombre, correo = correo, telefono = telefono, ciudad = ciudad, gusto = gusto)
		mail.send(msg)
		return nombre + correo
	else:
		return render_template('opinion.html')

@app.route('/registro', methods=['GET', 'POST'] )
def registro():
	if request.method == 'POST':
		name = request.form['name']
		paterno = request.form['paterno']
		materno = request.form['materno']
		fecha = request.form['fecha']
		edoCivil = request.form['edoCivil']
		ciudad = request.form['ciudad']
		correo = request.form['correo']
		fijo = request.form['fijo']
		celular = request.form['celular']
		conocimiento = request.form['conocimiento']
		lugarExperiencia = request.form['lugarExperiencia']
		perfil = request.form['perfil']
		file = request.files['cv']
	else:
		return render_template('registro.html')

	if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER']+"/cv",file.filename))
		extension = filename.split(".")
		extension = str(extension[1])
		source = UPLOAD_FOLDER+"/cv/"+filename
		destination  = UPLOAD_FOLDER+"/cv/"+name+paterno+materno+"."+extension
		os.rename(source,destination)
	else:
		flash('El archivo que subiste debe estar en formato pdf')
		return render_template('registro.html')

	#get random password
	randomPassword = get_random_string()

	#Build mail body and recipients
	msg = Message('Detalle de ingreso a la plataforma de ViSor', sender=("Registro existoso ViSor", "trabajoterminal2019a085@gmail.com"), recipients = [correo])
	msg.html = render_template('correo.html', value = name)
	#mail.send(msg)
	#Save user into database
	fullname = name + ' ' + paterno + ' ' + materno
	user = Usuario(name = fullname, fechaNacimiento = fecha, edoCivil = edoCivil, ciudad = ciudad, email = correo, telFijo = fijo, telCelular = celular, nameCV = destination, password = randomPassword , tempPassword = 1, medioEnterado = conocimiento, perfil = perfil, expPrevia = lugarExperiencia)
	db.session.add(user)
	db.session.commit()
	return render_template('signupSuccess.html')

@app.route('/usuarios')
def getUsers():
    users = Usuario.query.all()
    return render_template('dashboard/users.html', users = users)


@app.route('/changePassword')
def changePassword():
	name = 'Cristian'
	return render_template('changePassword.html', nombre = name)


@app.route('/ingresar', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


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
    nameCV = db.Column(db.String(50))
    password = db.Column(db.String(16))
    tempPassword = db.Column(db.Boolean)
    medioEnterado = db.Column(db.String(1))
    perfil = db.Column(db.String(1))
    expPrevia = db.Column(db.String(500))

    def __init__(self, name, fechaNacimiento, edoCivil, ciudad, email, telFijo, telCelular, nameCV, password, tempPassword, medioEnterado, perfil, expPrevia):
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
        self.expPrevia = expPrevia

    def __repr__(self):
        return '<User {}>'.format(self.name)




