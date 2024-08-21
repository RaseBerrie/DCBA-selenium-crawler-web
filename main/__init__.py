from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:root@localhost/searchdb'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'pool_recycle': 1800
}

db = SQLAlchemy(app)

from main.content import search
from main.nav import dropdown
from main.connect import crawler
from main.index import index

app.register_blueprint(search)
app.register_blueprint(dropdown)
app.register_blueprint(crawler)
app.register_blueprint(index)