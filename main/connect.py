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
            SELECT comp.company, req.key, b_def, g_def, b_git, g_git 
            FROM req_keys req
            JOIN list_subdomain sub ON req.key = sub.url
            JOIN list_rootdomain root ON sub.rootdomain = root.url
            JOIN list_company comp ON root.company = comp.company
            ORDER BY b_def, g_def, b_git, g_git;
            '''
    datas = database_query(query)

    return render_template('tab_one.html', datas=datas)