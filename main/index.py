from main import *

from flask import Blueprint, render_template
index = Blueprint('index', __name__, template_folder='templates/contents')

def read_output(pipe):
    while True:
        line = pipe.readline()
        if line:
            print(line.strip())
        else:
            break

@index.route('/')
@index.route('/dashboard')
def board():
    return render_template('dashboard.html')

@index.route('/<sidemenu>')
def contents(sidemenu):
    if sidemenu != "fileparses":
        return render_template('default_content.html')
    else:
        return render_template('file_content.html')