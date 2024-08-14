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
    query = '''
            SELECT lab.id AS company_id, lab.label
            FROM list_company comp
            JOIN res_data_label lab ON lab.label = comp.company
            '''
    categories = database_query(query)
    return render_template('first_level.html', categories=categories)


@dropdown.route('/secondlevel/<int:category_id>')
def second_level(category_id):
    if category_id == 0:
        return DROPTWO
    
    query = '''
            SELECT lab.id AS root_id, lab.label
            FROM list_rootdomain root
            JOIN res_data_label lab ON lab.label = root.url
            JOIN res_closure clo ON lab.id = clo.descendant
            WHERE clo.ancestor = {0}
            '''.format(category_id)
    categories = database_query(query)
    return render_template('second_level.html', categories=categories)


@dropdown.route('/thirdlevel/<int:category_id>')
def third_level(category_id):
    if category_id == 0:
        return DROPTHREE

    query = '''
            SELECT lab.id AS sub_id, lab.label
            FROM list_subdomain sub
            JOIN res_data_label lab ON lab.label = sub.url
            JOIN res_closure clo ON lab.id = clo.descendant
            WHERE clo.ancestor = {0}
            '''.format(category_id)
    categories = database_query(query)
    return render_template('third_level.html', categories=categories)