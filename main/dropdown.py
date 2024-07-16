from main import *
from functions.dbconnect import query_database

from flask import Blueprint, render_template
dropdown = Blueprint('dropdown', __name__, template_folder='templates/dropdown')

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
    query = f'''
    SELECT c.id AS company_id, c.company, COUNT(ccr.root_id) AS root_id_count
    FROM company c 
    JOIN conn_comp_root ccr ON c.id = ccr.comp_id
    GROUP BY c.id, c.company;
    '''
    categories = query_database(query)

    return render_template('first_level.html', categories=categories)

@dropdown.route('/secondlevel/<int:category_id>')
def second_level(category_id):
    if category_id == 0:
        return DROPTWO
    
    query = f'''
    SELECT rd.id AS root_id, rd.root_url, COUNT(crs.sub_id) AS sub_id_count
    FROM conn_comp_root cr
    JOIN rootdomain rd ON cr.root_id = rd.id
    LEFT JOIN conn_root_sub crs ON rd.id = crs.root_id
    WHERE cr.comp_id = %d
    GROUP BY rd.id, rd.root_url;
    ''' % (category_id)
    categories = query_database(query)
    return render_template('second_level.html', categories=categories)

@dropdown.route('/thirdlevel/<int:category_id>')
def third_level(category_id):
    if category_id == 0:
        return DROPTHREE

    query = '''
        SELECT sd.id, sd.sub_url
        FROM conn_root_sub cs
        JOIN subdomain sd ON cs.sub_id = sd.id
        WHERE cs.root_id = {0};
    '''.format(category_id)
    categories = query_database(query)
    return render_template('third_level.html', categories=categories)