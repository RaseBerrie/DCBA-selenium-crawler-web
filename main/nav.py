from main import *
from functions.utils import database_query

from flask import Blueprint, render_template
dropdown = Blueprint('dropdown', __name__, template_folder='templates/nav')


DROPTWO = '''<li class="dropdown-item">
            <a class="link-secondary link-underline-opacity-0" href="#" style="pointer-events: none;">
                회사명을 먼저 선택하세요.
            </a></li>'''
DROPTHREE = '''<li class="dropdown-item">
            <a class="link-secondary link-underline-opacity-0" href="#" style="pointer-events: none;">
                루트 도메인을 먼저 선택하세요.
            </a></li>'''


@dropdown.route('/firstlevel', methods=['GET'])
def first_level():
    query = 'SELECT * FROM list_company comp'
    categories = database_query(query)
    return render_template('first_level.html', categories=categories)


@dropdown.route('/secondlevel/<int:category_id>')
def second_level(category_id):
    if category_id == 0:
        return DROPTWO
    
    query = '''SELECT root.id, url FROM list_rootdomain root
    JOIN list_company comp ON root.company = comp.company
    WHERE comp.id = {0}'''.format(category_id)
    
    categories = database_query(query)
    return render_template('second_level.html', categories=categories)


@dropdown.route('/thirdlevel/<int:category_id>')
def third_level(category_id):
    if category_id == 0:
        return DROPTHREE

    query = '''SELECT sub.id, sub.url FROM list_subdomain sub
    JOIN list_rootdomain root ON sub.rootdomain = root.url
    WHERE root.id = {0} AND is_root = 0'''.format(category_id)
    categories = database_query(query)
    return render_template('third_level.html', categories=categories)