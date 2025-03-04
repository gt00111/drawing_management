import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String 
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "drawing.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

class Drawing(db.Model):
    __tablename__ = "drawing"
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(64), index=True)
    modelname = db.Column(db.String(64), index=True)
    drawingnumber = db.Column(db.String(64), index=True)
    version = db.Column(db.String(64), index=True)
    pagenumber = db.Column(db.String(64), index=True)

    def __init__(self, clientname, modelname, drawingnumber, version, pagenumber):
        self.clientname = clientname
        self.modelname = modelname
        self.drawingnumber = drawingnumber
        self.version = version
        self.pagenumber = pagenumber


    def __repr__(self):
        return f"client: {self.client}" 
    
if __name__ == "__main__":
    app.run(debug=True)