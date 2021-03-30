from flask_app import app
from flask_sqlalchemy import SQLAlchemy

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


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    fechaNacimiento = db.Column(db.Date)
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
      return '<User %d>' % self.id