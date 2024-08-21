# 고정변수
NORESULT = '<tr><td colspan=5>검색 결과가 없습니다.<span id="count-result" style="display: none;">0</span></td></tr>'
SELECTQUERY = 'SELECT * FROM temp_searchresult'
COUNTQUERY = 'SELECT count(*) FROM temp_searchresult'

from urllib.parse import unquote
from json import loads
from io import BytesIO

from main import *
from functions.utils import database_query, database_connect, def_temp_table, file_temp_table, data_fining, file_fining
import pandas as pd

from flask import Blueprint, Response, request, render_template, jsonify
search = Blueprint('search', __name__, template_folder='templates/content')

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
    else:
        status = False

    per_page = 15
    offset = (page - 1) * per_page

    conn = database_connect()
    cur = conn.cursor()

    query_dat = ""
    query_count = ""

    if sidemenu == "fileparse":
        file_temp_table(cur, id, status)
        if tag:
            query_dat += f"SELECT se, subdomain, filetype, title, url, data, moddate FROM temp_fileresult WHERE filetype = '%s'" % (tag)
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE filetype = '%s'" % (tag)
        else:
            query_dat += f"SELECT se, subdomain, filetype, title, url, data, moddate FROM temp_fileresult"
            query_count += f"SELECT count(*) FROM temp_fileresult"

    elif sidemenu == "expose":
        def_temp_table(cur, id, status)
        if tag:
            query_dat += SELECTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE t_expose.restype = '%s'" % (tag)
            query_count += COUNTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE t_expose.restype = '%s'" % (tag)
        else:
            query_dat += SELECTQUERY + f" WHERE tags = 'expose'"
            query_count += COUNTQUERY + f" WHERE tags = 'expose'"

    elif sidemenu == "gitsearch":
        def_temp_table(cur, id, status, git=True)
        query_dat += SELECTQUERY
        query_count += COUNTQUERY

    else:
        def_temp_table(cur, id, status)
        if sidemenu == "content":
            query_dat = SELECTQUERY
            query_count = COUNTQUERY
        
        elif sidemenu == "loginpage":
            query_dat += SELECTQUERY + f" WHERE tags = 'login'"
            query_count += COUNTQUERY + f" WHERE tags = 'login'"
        
        elif sidemenu == "adminpage":
            query_dat += SELECTQUERY + f" WHERE tags = 'admin'"
            query_count += COUNTQUERY + f" WHERE tags = 'admin'"

    if not filedownload:
        query_dat = query_dat + " LIMIT %s OFFSET %s" % (per_page, offset)

    cur.execute(query_dat)
    data = cur.fetchall()
    
    cur.execute(query_count)
    count = cur.fetchone()

    if len(data) == 0:
            return NORESULT

    cur.close()
    conn.close()

    if filedownload:
        if sidemenu == "fileparse":
            head = ["SearchEngine", "Subdomain", "FileType", "Title", "URL", "Contents"]
            result = file_fining(data)
        else:
            head = ["SearchEngine", "Subdomain", "Title", "URL", "Contents"]
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

    if sidemenu == "fileparse":
        return render_template('file_results.html', datas=file_fining(data), count=count[0], enumerate=enumerate, page=page)
    else:
        return render_template('default_results.html', datas=data_fining(data), count=count[0], enumerate=enumerate, page=page)

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
    else:
        status = False
        
    per_page = 15
    offset = (page - 1) * per_page

    conn = database_connect()
    cur = conn.cursor()

    data = []
    count = [0, ]

    query_dat = ""
    query_count = ""

    if sidemenu == "fileparse":
        file_temp_table(cur, id, status)
        if menu and key and tag:
            query_dat += f"SELECT se, subdomain, filetype, title, url, data, moddate FROM temp_fileresult WHERE {menu} LIKE %s AND filetype = '%s'" % (f'"%{key}%"', tag)
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE {menu} LIKE %s AND filetype = '%s'" % (f'"%{key}%"', tag)

        elif menu and key:
            query_dat += f"SELECT se, subdomain, filetype, title, url, data, moddate FROM temp_fileresult WHERE {menu} LIKE %s" % (f'"%{key}%"')
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE {menu} LIKE %s" % (f'"%{key}%"')
            
        elif tag:
            query_dat += f"SELECT se, subdomain, filetype, title, url, data, moddate FROM temp_fileresult WHERE filetype = '%s'" % (tag)
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE filetype = '%s'" % (tag)

    elif sidemenu == "expose":
        def_temp_table(cur, id, status)
        if menu and key and tag:
            #sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE t_expose.restype = '%s'"
            query_dat += SELECTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE t_expose.restype = '%s' AND sr.{menu} LIKE %s AND tags = 'expose'" % (tag, f'"%{key}%"')
            query_count += COUNTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE t_expose.restype = '%s' AND sr.{menu} LIKE %s AND tags = 'expose'" % (tag, f'"%{key}%"')

        elif menu and key:
            query_dat += SELECTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE sr.{menu} LIKE %s" % (f'"%{key}%"')
            query_count += COUNTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE sr.{menu} LIKE %s" % (f'"%{key}%"')

        elif tag:
            query_dat += SELECTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE t_expose.restype = '%s'" % (tag)
            query_count += COUNTQUERY + f" sr JOIN res_tags_expose t_expose ON t_expose.url = sr.res_url WHERE t_expose.restype = '%s'" % (tag)

    elif sidemenu == "gitsearch":
        def_temp_table(cur, id, status, git=True)
        query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')
        query_count += COUNTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')

    else:
        if menu and key:
            def_temp_table(cur, id, status)
            if sidemenu == "content":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')

            elif sidemenu == "loginpage":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'login'" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'login'" % (f'"%{key}%"')
            
            elif sidemenu == "adminpage":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'admin'" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'admin'" % (f'"%{key}%"')

            elif sidemenu == "expose":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'expose'" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'expose'" % (f'"%{key}%"')

    query_dat = query_dat + " LIMIT %s OFFSET %s" % (per_page, offset)
    cur.execute(query_dat)
    data = cur.fetchall()
        
    cur.execute(query_count)
    count = cur.fetchone()
    
    if len(data) == 0:
        return NORESULT

    cur.close()
    conn.close()

    if filedownload:
        if sidemenu == "fileparse":
            head = ["SearchEngine", "Subdomain", "FileType", "Title", "URL", "Contents"]
            result = file_fining(data)
        else:
            head = ["SearchEngine", "Subdomain", "Title", "URL", "Contents"]
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

    if sidemenu == "fileparse":
        return render_template('file_results.html', datas=file_fining(data), count=count[0], enumerate=enumerate, page=page)
    else:
        return render_template('default_results.html', datas=data_fining(data), count=count[0], enumerate=enumerate, page=page)

@search.route('/dashboard/default', methods=['GET'])
def dashboard():
    query = 'SELECT * FROM list_company'
    ids = database_query(query)
    count = len(ids)

    data = []
    query = '''
    SELECT 	COUNT(*),
    COUNT(CASE WHEN b_def LIKE 'finished' AND b_git LIKE 'finished' THEN 1 END),
    COUNT(CASE WHEN g_def LIKE 'finished' AND g_git LIKE 'finished' THEN 1 END)
    FROM 	req_keys'''    
    data += database_query(query)
    
    for i in range(count):
        query = f'''
        SELECT '{ids[i][1]}',
        COUNT(*) AS totalcount,
        COUNT(CASE WHEN tags NOT LIKE '' AND tags NOT LIKE 'public' THEN 1 END) AS pub,
        COUNT(CASE WHEN FIND_IN_SET('login', tags) THEN 1 END) AS login,
        COUNT(CASE WHEN FIND_IN_SET('admin', tags) THEN 1 END) AS admin,
        COUNT(CASE WHEN FIND_IN_SET('file', tags) THEN 1 END) AS file,
        COUNT(CASE WHEN FIND_IN_SET('expose', tags) THEN 1 END) AS expose,
        COUNT(CASE WHEN FIND_IN_SET('git', tags) THEN 1 END) AS git
        FROM res_data data
        JOIN list_subdomain sub ON sub.url = data.subdomain
        JOIN list_rootdomain root ON root.url = sub.rootdomain
        JOIN list_company comp ON root.company = comp.company
        WHERE comp.id = {ids[i][0]}
        '''
        data += database_query(query)

    return jsonify(data)