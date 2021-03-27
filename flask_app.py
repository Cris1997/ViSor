
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import string

UPLOAD_FOLDER='/home/CristianDeloya/mysite/static/uploads/'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


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


@app.route('/registro', methods=['GET', 'POST'] )
def registro():
	if request.method == 'POST':
		name = request.form['name']
		paterno = request.form['paterno']
		materno = request.form['materno']
		fecha = request.form['fecha']
		ciudad = request.form['ciudad']
		correo = request.form['correo']
		fijo   = request.form['fijo']
		celular = request.form['celular']
		conocimiento = request.form['conocimiento']
		lugarExperiencia = request.form['lugarExperiencia']
		perfil = request.form['perfil']
		file = request.files['cv']
		if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
		    filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            extension=filename.split(".")
            extension=str(extension[1])
            source=UPLOAD_FOLDER+"/"+filename
            destination=UPLOAD_FOLDER+"/"+"HOLA"+"."+extension
            os.rename(source,destination)
            flash(file.filename+" saved succesfully")
		return conocimiento
	else:
		return render_template('registro.html')



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