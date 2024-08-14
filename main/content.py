# 고정변수
NORESULT = '<tr><td colspan=5>검색 결과가 없습니다.<span id="count-result" style="display: none;">0</span></td></tr>'
SELECTQUERY = f'SELECT * FROM temp_searchresult'
COUNTQUERY = f'SELECT count(*) FROM temp_searchresult'

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

    if sidemenu == "fileparses":
        file_temp_table(cur, id, status)
        if tag:
            query_dat += f"SELECT se, filetype, title, url, data, moddate FROM temp_fileresult WHERE filetype = '%s'" % (tag)
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE filetype = '%s'" % (tag)
        else:
            query_dat += f"SELECT se, filetype, title, url, data, moddate FROM temp_fileresult"
            query_count += f"SELECT count(*) FROM temp_fileresult"

    elif sidemenu == "neednot":
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
        if sidemenu == "fileparses":
            head = ["SearchEngine", "FileType", "Title", "URL", "Contents"]
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

    if sidemenu == "fileparses":
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

    if sidemenu == "fileparses":
        file_temp_table(cur, id, status)
        if menu and key and tag:
            query_dat += f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult WHERE {menu} LIKE %s AND filetype = '%s'" % (f'"%{key}%"', tag)
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE {menu} LIKE %s AND filetype = '%s'" % (f'"%{key}%"', tag)

        elif menu and key:
            query_dat += f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult WHERE {menu} LIKE %s" % (f'"%{key}%"')
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE {menu} LIKE %s" % (f'"%{key}%"')
            
        elif tag:
            query_dat += f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult WHERE filetype = '%s'" % (tag)
            query_count += f"SELECT count(*) FROM temp_fileresult WHERE filetype = '%s'" % (tag)

        query_dat = query_dat + " LIMIT %s OFFSET %s" % (per_page, offset)
        cur.execute(query_dat)
        data = cur.fetchall()


    elif sidemenu == "neednot":
        def_temp_table(cur, id, status)
        if menu and key and tag:
            query_dat += SELECTQUERY + f" sr JOIN list_neednot lnn ON lnn.id = sr.id WHERE lnn.restype = '%s' AND sr.{menu} LIKE %s AND tags = 'is_neednot'" % (tag, f'"%{key}%"')
            query_count += COUNTQUERY + f" sr JOIN list_neednot lnn ON lnn.id = sr.id WHERE lnn.restype = '%s' AND sr.{menu} LIKE %s AND tags = 'is_neednot'" % (tag, f'"%{key}%"')

        elif menu and key:
            query_dat += SELECTQUERY + f" sr JOIN list_neednot lnn ON lnn.id = sr.id WHERE sr.{menu} LIKE %s" % (f'"%{key}%"')
            query_count += COUNTQUERY + f" sr JOIN list_neednot lnn ON lnn.id = sr.id WHERE sr.{menu} LIKE %s" % (f'"%{key}%"')

        elif tag:
            query_dat += SELECTQUERY + f" sr JOIN list_neednot lnn ON lnn.id = sr.id WHERE lnn.restype = '%s'" % (tag)
            query_count += COUNTQUERY + f" sr JOIN list_neednot lnn ON lnn.id = sr.id WHERE lnn.restype = '%s'" % (tag)

        query_dat = query_dat + " LIMIT %s OFFSET %s" % (per_page, offset)
        cur.execute(query_dat)
        data = cur.fetchall()

    else:
        if menu and key:
            def_temp_table(cur, id, status)
            if sidemenu == "content":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')

            elif sidemenu == "loginpage":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_login'" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_login'" % (f'"%{key}%"')
            
            elif sidemenu == "adminpage":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_admin'" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_admin'" % (f'"%{key}%"')

            elif sidemenu == "neednot":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_neednot'" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_neednot'" % (f'"%{key}%"')

            elif sidemenu == "gitsearch":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_github'" % (f'"%{key}%"')
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_github'" % (f'"%{key}%"')

            elif sidemenu == "jssearch":
                query_dat += SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_js'"
                query_count += COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_js'"

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
        if sidemenu == "fileparses":
            head = ["SearchEngine", "FileType", "Title", "URL", "Contents"]
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

    if sidemenu == "fileparses":
        return render_template('file_results.html', datas=file_fining(data), count=count[0], enumerate=enumerate, page=page)
    else:
        return render_template('default_results.html', datas=data_fining(data), count=count[0], enumerate=enumerate, page=page)

@search.route('/dashboard/default', methods=['GET'])
def dashboard():
    query = 'SELECT id FROM list_company'
    ids = database_query(query)
    count = len(ids)

    data = []
    query = '''
        SELECT 	COUNT(*),
                COUNT(CASE WHEN Bing NOT LIKE 'N' AND GitHub_Bing NOT LIKE 'N' THEN 1 END),
                COUNT(CASE WHEN Google NOT LIKE 'N' AND GitHub_Google NOT LIKE 'N' THEN 1 END)
        FROM 	search_key
        '''
    data += database_query(query)
    
    for i in range(count):
        id = ids[i][0]

        query = '''
        SELECT 	cmp.company,
                COUNT(*) AS totalcount,
                COUNT(CASE WHEN tags NOT LIKE '' AND tags NOT LIKE 'filter' THEN 1 END) AS tagcount,
                COUNT(CASE WHEN FIND_IN_SET('is_login', tags) THEN 1 END) AS logincount,
                COUNT(CASE WHEN FIND_IN_SET('is_admin', tags) THEN 1 END) AS admincount,
                COUNT(CASE WHEN FIND_IN_SET('is_file', tags) THEN 1 END) AS filecount,
                COUNT(CASE WHEN FIND_IN_SET('is_neednot', tags) THEN 1 END) AS nncount,
                COUNT(CASE WHEN FIND_IN_SET('is_github', tags) THEN 1 END) AS gitcount
        FROM 	list_company cmp
        JOIN 	conn_comp_root ccr ON cmp.id = ccr.comp_id
        JOIN 	conn_root_sub crs ON ccr.root_id = crs.root_id
        JOIN 	conn_sub_res csr ON crs.sub_id = csr.sub_id
        JOIN 	search_result sr ON csr.res_id = sr.id
        WHERE   cmp.id = %s;
        '''
        data += database_query(query, (id, ))

    return jsonify(data)