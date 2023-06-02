from email.mime import image
import sqlite3
from sqlite3 import DataError
from sqlite3 import Error
from flask import  Flask, render_template, request, jsonify,current_app
from werkzeug.utils import secure_filename
from pathlib import Path

import os
app = Flask(__name__)
UPLOAD_FOLDER = '\\static\\temporal'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def conexion():
 try:
    con = sqlite3.connect('datosPeliculas.db')
    return con
 except Error:
   print(Error)



def init_db():
    with app.app_context():
        db = conexion()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

    




 
