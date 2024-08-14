from flask import Flask

app = Flask(__name__)

from main.content import search
from main.nav import dropdown
from main.connect import crawler
from main.index import index

app.register_blueprint(search)
app.register_blueprint(dropdown)
app.register_blueprint(crawler)
app.register_blueprint(index)