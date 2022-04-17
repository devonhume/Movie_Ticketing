from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4

# Create Flask App

app = Flask(__name__)

# Create Flask App
app = Flask(__name__)

# Configure QLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plotter_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set Secret Keys
app.config['SECRET_KEY'] = 'AllTheWorldsAPhage'
app.config['WTF_CSRF_SECRET_KEY'] = 'ARoseByAnyOtherNomenclature'

# Create Database, Bootstrap
db = SQLAlchemy(app)
bootstrap = Bootstrap4(app)