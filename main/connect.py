from main import *
from flask import Blueprint, render_template

from functions.models import ReqKeys, ListSub, ListRoot
from sqlalchemy import desc

crawler = Blueprint('crawler', __name__, template_folder='templates/connect', url_prefix="/crawler")

@crawler.route('/')
def main():
    return render_template('crawler_start.html')

@crawler.route('/table')
def reload():
    query = db.session.query(ReqKeys, ListRoot)
    query = query.join(ListSub, ListSub.url == ReqKeys.key)\
        .join(ListRoot, ListRoot.url == ListSub.rootdomain)
    datas = query.order_by(desc(ReqKeys.id))

    return render_template('tab_one.html', datas=datas)