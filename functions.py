import random
import string
import datetime

#Verificar que el usario tenga la mayoria de edad
def verificaEdad(fechaStr):

    format_str = '%d/%m/%Y' # The format
    datetime_obj = datetime.datetime.strptime(fechaStr, format_str).date()

    hoy = datetime.date.today()

    if hoy < datetime_obj:
        return 0
    else:
        ano = datetime_obj.year
        mes = datetime_obj.month
        dia = datetime_obj.day

        fecha = datetime_obj
        edad = 0
        while fecha < hoy:
            edad += 1
            fecha = datetime.date(ano+edad, mes, dia)

        if edad >= 18:
            return True
        else:
            return False

#Funcion para verificar que el archivo a subir es válido
def allowed_file(filename, allowedExtensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtensions

#Funcion para generarle un password temporal
def get_random_string():
    # With combination of lower and upper case
    return ''.join(random.choice(string.ascii_letters) for i in range(8))
