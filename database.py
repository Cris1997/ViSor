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


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
