NORESULT = '<tr><td colspan=5>검색 결과가 없습니다.<span id="count-result" style="display: none;">0</span></td></tr>'

from urllib.parse import unquote
from json import loads
from sqlalchemy import and_, or_, func
from io import BytesIO

from main import *
from functions.utils import def_query, file_query, exp_query, data_fining, file_fining
from functions.models import ResDefData, ResGitData, ResCacheData, ListComp, ListSub, ListRoot, TagExp, TagFile, ReqKeys

import pandas as pd

from flask import Blueprint, Response, request, render_template, jsonify
search = Blueprint('search', __name__, template_folder='templates/content')

menu_dict = {"loginpage": "login", "adminpage": "admin", "expose": "expose"}
@search.route('/<sidemenu>/default', methods=['GET'])
def main(sidemenu):
    # 서브메뉴 접속 후 첫 페이지 로드
    tag = request.args.get('tag', '')
    page = int(request.args.get('page', 1))
    filedownload = request.args.get('filedownload', False, type=bool)
    
    if request.cookies.get('topMenu') != None:
        id = loads(unquote(request.cookies.get('topMenu')))
    else:
        id = {"comp": [0]}

    if request.cookies.get('status') != None:
        status = loads(unquote(request.cookies.get('status')))["filter"]
        searchengine = loads(unquote(request.cookies.get('status')))["searchengine"]
    else:
        status = False
        
    if searchengine not in ["All", "G", "B"]:
        searchengine = "All"

    per_page = 15
    offset = (page - 1) * per_page

    if sidemenu == "fileparse":
        query = file_query(id, status)
        if tag: query = query.filter(TagFile.filetype == tag)

    elif sidemenu == "gitsearch":
        query = def_query(id, status, searchengine=searchengine, git=True)

    elif sidemenu == "expose":
        query = exp_query(id, searchengine)
        if tag:
            query = query.filter(TagExp.restype == tag)
        else:
            query = query.filter(ResDefData.tags == 'expose')

    else:
        query = def_query(id, status, searchengine=searchengine)
        if sidemenu == "content":
            query = query.filter(or_(ResDefData.tags == '', ResDefData.tags == 'public'))

        elif sidemenu in ["loginpage", "adminpage"]:
            query = query.filter(ResDefData.tags == menu_dict[sidemenu])

    count = query.count()
    if count == 0: return NORESULT

    if filedownload:
        data = query.all()
        if sidemenu == "fileparse":
            head = ["SearchEngine", "Port", "Subdomain", "FileType", "Title", "URL", "Contents"]
            result = file_fining(data)
        else:
            head = ["SearchEngine", "Port", "Subdomain", "Title", "URL", "Contents"]
            result = data_fining(data)

        output_stream = BytesIO()
        df = pd.DataFrame(result, columns=head)

        df.to_csv(output_stream, index=False, escapechar='\\',
                  encoding="utf-8-sig", sep=",")

        output_stream.seek(0)
        response = Response(
            output_stream.getvalue(),
            mimetype='text/csv',
            content_type='text/csv',
        )
        response.headers["Content-Disposition"] = "attachment; filename=database_export.csv"
        output_stream.close()
        return response
    else:
        data = query.limit(per_page).offset(offset).all()

    if sidemenu == "fileparse":
        return render_template('file_results.html', datas=file_fining(data), count=count, enumerate=enumerate, page=page)
    else:
        return render_template('default_results.html', datas=data_fining(data), count=count, enumerate=enumerate, page=page)

@search.route('/<sidemenu>/result', methods=['GET'])
def result(sidemenu):
    # 검색 후 페이지 로드
    tag = request.args.get('tag', '')
    menu = request.args.get('menu', '')
    key = request.args.get('key', '')

    filedownload = request.args.get('filedownload', False, type=bool)
    page = int(request.args.get('page', 1))

    if request.cookies.get('topMenu') != None:
        id = loads(unquote(request.cookies.get('topMenu')))
    else:
        id = {"comp": [0]}

    if request.cookies.get('status') != None:
        status = loads(unquote(request.cookies.get('status')))["filter"]
        searchengine = loads(unquote(request.cookies.get('status')))["searchengine"]
    else:
        status = False
        searchengine = "All"
        
    per_page = 15
    offset = (page - 1) * per_page

    if sidemenu == "fileparse":
        query = file_query(id, status)
        if menu and key:
            query = query.filter(getattr(TagFile, menu).like(f'%{key}%'))
        if tag:
            query = query.filter(TagFile.filetype == tag)

    else:
        if sidemenu == "gitsearch":
            query = def_query(id, status, searchengine=searchengine, git=True)
            query = query.filter(getattr(ResGitData, menu).like(f'%{key}%'))

        else:
            if menu and key:
                if sidemenu in ["loginpage", "adminpage"]:
                    query = def_query(id, status, searchengine=searchengine)
                    query = query.filter(ResDefData.tags == menu_dict[sidemenu])

                elif sidemenu == "content":
                    query = def_query(id, status, searchengine=searchengine)
                    query = query.filter(or_(ResDefData.tags == '', ResDefData.tags == 'public'))
                    
                elif sidemenu == "expose":
                    query = exp_query(id, searchengine)
                    if tag:
                        query = query.filter(TagExp.restype == tag)
                    else:
                        query = query.filter(ResDefData.tags == 'expose')

                query = query.filter(getattr(ResDefData, menu).like(f'%{key}%'))

    count = query.count()
    if count == 0: return NORESULT

    if filedownload:
        if sidemenu == "fileparse":
            head = ["SearchEngine", "Port", "Subdomain", "FileType", "Title", "URL", "Contents"]
            result = file_fining(data)
        else:
            head = ["SearchEngine", "Port", "Subdomain", "Title", "URL", "Contents"]
            result = data_fining(data)

        output_stream = BytesIO()
        df = pd.DataFrame(result, columns=head)

        df.to_csv(output_stream, index=False, escapechar='\\',
                  encoding="utf-8-sig", sep=",")

        output_stream.seek(0)
        response = Response(
            output_stream.getvalue(),
            mimetype='text/csv',
            content_type='text/csv',
        )
        response.headers["Content-Disposition"] = "attachment; filename=database_export.csv"
        output_stream.close()
        return response
    else:
        data = query.limit(per_page).offset(offset).all()

    if sidemenu == "fileparse":
        return render_template('file_results.html', datas=file_fining(data), count=count, enumerate=enumerate, page=page)
    else:
        return render_template('default_results.html', datas=data_fining(data), count=count, enumerate=enumerate, page=page)

@search.route('/dashboard/default', methods=['GET'])
def dashboard():
    data = []

    key_list = []
    query = db.session.query(ReqKeys)

    key_list.append(query.count())
    key_list.append(query.filter(and_(ReqKeys.b_def == 'finished', ReqKeys.b_git == 'finished')).count())
    key_list.append(query.filter(and_(ReqKeys.g_def == 'finished', ReqKeys.g_git == 'finished')).count())

    data.append(key_list)
    
    comp_list = db.session.query(ListComp).all()
    results = db.session.query(
        ListComp.company,
        ResDefData.tags,
        func.count(ResDefData.id).label('tag_count')
    ).join(ListSub, ListSub.url == ResDefData.subdomain)\
        .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
            .join(ListComp, ListComp.company == ListRoot.company)\
                .filter(ListComp.id.in_([comp.id for comp in comp_list]))\
                    .group_by(ListComp.company, ResDefData.tags).all()

    comp_data = {}
    for company, tag, count in results:
        if company not in comp_data:
            comp_data[company] = {'total': 0, 'non_public': 0, 'login': 0, 'admin': 0, 'file': 0, 'expose': 0, 'git': 0}
        
        comp_data[company]['total'] += count
        
        if tag not in ['public', '']:
            comp_data[company]['non_public'] += count
        
        if tag in comp_data[company]:
            comp_data[company][tag] = count
    
    for comp in comp_list:
        if comp.company in comp_data.keys():
            company = comp.company
            if comp_data[company]['non_public'] > 0:    
                tmp = [
                    company,
                    comp_data[company]['total'],
                    comp_data[company]['non_public'],
                    comp_data[company]['login'],
                    comp_data[company]['admin'],
                    comp_data[company]['file'],
                    comp_data[company]['expose'],
                    comp_data[company]['git']
                ]
                data.append(tmp)

    return jsonify(data)

@search.route('/cache', methods=['GET'])
def findcache():
    cache_url = request.args.get('url')
    query = db.session.query(ResCacheData.cache).filter(ResCacheData.url == cache_url)

    html_cache = query.one()
    return html_cache[0].decode('utf-8')