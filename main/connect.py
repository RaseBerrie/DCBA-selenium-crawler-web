from main import *
from functions.utils import database_query
from flask import Blueprint, render_template

crawler = Blueprint('crawler', __name__, template_folder='templates/connect', url_prefix="/crawler")

@crawler.route('/')
def main():
    return render_template('crawler_start.html')

@crawler.route('/table')
def reload():
    query = '''
            SELECT comp.company, req.key, g_def, b_def, g_git, b_git 
            FROM res_data_label lab
            JOIN req_keys req ON lab.label = req.key
            JOIN res_closure clo ON lab.id = clo.descendant
            JOIN list_company comp ON comp.id = clo.ancestor
            WHERE depth > 0 AND ancestor IN (select id from list_company)
            ORDER BY req.id DESC;
            '''
    datas = database_query(query)

    return render_template('tab_one.html', datas=datas)