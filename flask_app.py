
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


UPLOAD_FOLDER='static/uploads/'


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024




@app.route('/')
def index():
	#return render_template('upload.html')
	#return render_template('prueba.html')
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
		genero  = request.form['genero']
		edoCivil =  request.form['edoCivil']
		calle  =  request.form['calle']
		numInt =  request.form['numInt']
		numExt =  request.form['numExt']
		ciudad  =  request.form['ciudad']
		code =  request.form['code']
		email =  request.form['email']
		number =  request.form['number']
		return name
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