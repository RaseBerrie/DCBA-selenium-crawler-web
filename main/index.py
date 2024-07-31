from main import *

from flask import Blueprint, render_template
index = Blueprint('index', __name__, template_folder='templates/contents')

@index.route('/')
@index.route('/dashboard')
def board():
    return render_template('dashboard.html')

@index.route('/others')
def others():
    return render_template('others.html')

@index.route('/<sidemenu>')
def contents(sidemenu):
    if sidemenu != "fileparses":
        return render_template('default_content.html')
    else:
        return render_template('file_content.html')