from flask_app import db


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