import random
import string



#Funcion para verificar que el archivo a subir es válido
def allowed_file(filename, allowedExtensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtensions

#Funcion para generarle un password temporal
def get_random_string():
    # With combination of lower and upper case
    return ''.join(random.choice(string.ascii_letters) for i in range(8))
