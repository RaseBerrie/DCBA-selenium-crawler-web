from main import *
from functions.models import ListComp, ListRoot, ListSub

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
    categories = db.session.query(ListComp).all()
    return render_template('first_level.html', categories=categories)

@dropdown.route('/secondlevel/<int:category_id>')
def second_level(category_id):
    if category_id == 0:
        return DROPTWO
    
    query = db.session.query(ListRoot)
    query = query.join(ListComp, ListComp.company == ListRoot.company)
    categories = query.filter(ListComp.id == category_id).all()

    return render_template('second_level.html', categories=categories)

@dropdown.route('/thirdlevel/<int:category_id>')
def third_level(category_id):
    if category_id == 0:
        return DROPTHREE

    query = db.session.query(ListSub)
    query = query.join(ListRoot, ListRoot.url == ListSub.rootdomain)
    categories = query.filter(ListRoot.id == category_id).all()

    return render_template('third_level.html', categories=categories)