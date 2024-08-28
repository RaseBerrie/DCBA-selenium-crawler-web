from main import *
from flask import Blueprint, render_template

from functions.models import ReqKeys, ListSub, ListRoot

crawler = Blueprint('crawler', __name__, template_folder='templates/connect', url_prefix="/crawler")

@crawler.route('/')
def main():
    return render_template('crawler_start.html')

@crawler.route('/table')
def reload():
    query = db.session.query(ReqKeys, ListRoot)
    query = query.join(ListSub, ListSub.url == ReqKeys.key)\
        .join(ListRoot, ListRoot.url == ListSub.rootdomain)
    datas = query.order_by(ReqKeys.b_def).order_by(ReqKeys.g_def)\
        .order_by(ReqKeys.b_git).order_by(ReqKeys.g_git).all()

    return render_template('tab_one.html', datas=datas)