from main import *
from flask import Blueprint, render_template, jsonify

from functions.models import ReqKeys, ReqStat, ListSub, ListRoot
from sqlalchemy import func, desc, and_, or_
from datetime import datetime

import json

crawler = Blueprint('crawler', __name__, template_folder='templates/connect', url_prefix="/crawler")
result = {"b_def": None, "g_def": None, "b_git": None, "g_git": None}

@crawler.route('/')
def main():
    query = db.session.query(ReqKeys)\
        .filter(~and_(ReqKeys.b_def_status == "none", ReqKeys.b_git_status == "none",
                      ReqKeys.g_def_status == "none", ReqKeys.g_git_status == "none"))
    count = query.count()
    if count == 0:
        data = db.session.query(ReqStat).all()
        
        google_data, bing_data = data[0].last_request, data[1].last_request
        now = datetime.now()        
        td = min(now-google_data, now-bing_data)

        return render_template('crawler_start.html', google_data = google_data, bing_data = bing_data,
                               time_diff = str(td).replace(' day,', '일').replace(' days,', '일').split(':'))
    else:
        return render_template('crawler_inprocess.html')

@crawler.route('/table')
def reload():
    query = db.session.query(ReqKeys, ListRoot)
    query = query.join(ListSub, ListSub.url == ReqKeys.key)\
                 .join(ListRoot, ListRoot.url == ListSub.rootdomain)
    datas = query.order_by(desc(ReqKeys.id))

    return render_template('tab_one.html', datas=datas)

@crawler.route('/process')
def processor():    
    for key in result.keys():
        killed_count = db.session.query(func.count(ReqKeys.id)).filter((getattr(ReqKeys, key + "_status") == "killed")).scalar()
        alive_count = db.session.query(func.count(ReqKeys.id)).filter((getattr(ReqKeys, key + "_status") == "running")).scalar()
        
        if killed_count > 0 and alive_count == 0:
            result[key] = "killed"
        else:
            finished_condition = and_(getattr(ReqKeys, key) == "finished", getattr(ReqKeys, key + "_status") == "done")
            notstarted_condition = and_(getattr(ReqKeys, key) == "notstarted", getattr(ReqKeys, key + "_status") == "killed")

            numerator_subquery = db.session.query(func.count(ReqKeys.id).label("numerator"))\
                                           .filter(or_(finished_condition, notstarted_condition)).scalar_subquery()
            
            denominator_subquery = db.session.query(func.count(ReqKeys.id).label("denominator"))\
                                             .filter((getattr(ReqKeys, key + "_status") != "none"))\
                                             .scalar_subquery()
            
            ratio_query = db.session.query(func.coalesce(numerator_subquery / func.nullif(denominator_subquery, 0), -1))
            ratio = db.session.execute(ratio_query).scalar()
            
            if ratio >= 0:
                result[key] = int(ratio * 100)
            else: result[key] = int(ratio)
            
    return jsonify(json.dumps(result))

@crawler.route('/finish')
def finish():
    try:
        for key in result.keys():
            target_key = db.session.query(ReqKeys).filter(~(getattr(ReqKeys, key + "_status") == "none"))
            target_key.update({key + "_status": "none"})

            db.session.commit()
            result[key] = None
        return jsonify(json.dumps({"status": "success"}))
    
    except:
        return jsonify(json.dumps({"status": "fail"}))
