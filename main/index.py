from main import *

import json
import urllib.parse as parse

from flask import Blueprint, render_template, make_response, request
index = Blueprint('index', __name__, template_folder='templates/frame')

@index.route('/')
@index.route('/dashboard')
def board():
    if request.cookies.get("status") is None:
        cookie = {"crawler":False,"filter":False}
        resp = make_response(render_template('dashboard.html'))

        resp.set_cookie("status", parse.quote(json.dumps(cookie)))
        return resp
    else:
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