from flask import Flask

app = Flask(__name__)

from main.search import search
from main.dropdown import dropdown
from main.crawler import crawler
from main.index import index

app.register_blueprint(search)
app.register_blueprint(dropdown)
app.register_blueprint(crawler)
app.register_blueprint(index)