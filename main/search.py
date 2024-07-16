# 고정변수
NORESULT = '<tr><td colspan={0}>검색 결과가 없습니다.<span id="count-result" style="display: none;">0</span></td></tr>'
SELECTQUERY = f'SELECT * FROM temp_searchresult'
COUNTQUERY = f'SELECT count(*) FROM temp_searchresult'

from urllib.parse import unquote
from json import loads
from io import BytesIO

from main import *
from functions.dbconnect import query_database, database_connect, def_temp_table, file_temp_table, data_fining, file_fining
import pandas as pd

from flask import Blueprint, Response, request, render_template, jsonify
search = Blueprint('search', __name__, template_folder='templates/contents')

@search.route('/<sidemenu>/default', methods=['GET'])
def main(sidemenu):
    # 서브메뉴 접속 후 첫 페이지 로드
    tag = request.args.get('tag', '')
    page = int(request.args.get('page', 1))
    filedownload = request.args.get('filedownload', False, type=bool)
    id = loads(unquote(request.cookies.get('topMenu')))

    per_page = 30
    offset = (page - 1) * per_page

    conn = database_connect()
    cur = conn.cursor()

    if sidemenu == "fileparses":
        file_temp_table(cur, id)
        if tag:
            query_dat = f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult WHERE filetype = '%s'" % (tag)
            query_count = f"SELECT count(*) FROM temp_fileresult WHERE filetype = '%s'" % (tag)
        else:
            query_dat = f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult"
            query_count = f"SELECT count(*) FROM temp_fileresult"

    else:
        def_temp_table(cur, id)
        if sidemenu == "content":
            query_dat = SELECTQUERY
            query_count = COUNTQUERY
        
        elif sidemenu == "loginpage":
            query_dat = SELECTQUERY + f" WHERE tags = 'is_login'"
            query_count = COUNTQUERY + f" WHERE tags = 'is_login'"
        
        elif sidemenu == "adminpage":
            query_dat = SELECTQUERY + f" WHERE tags = 'is_admin'"
            query_count = COUNTQUERY + f" WHERE tags = 'is_admin'"

        elif sidemenu == "neednot":
            query_dat = SELECTQUERY + f" WHERE tags = 'is_neednot'"
            query_count = COUNTQUERY + f" WHERE tags = 'is_neednot'"

        elif sidemenu == "gitsearch":
            query_dat = SELECTQUERY + f" WHERE tags = 'is_github'"
            query_count = COUNTQUERY + f" WHERE tags = 'is_github'"

        elif sidemenu == "jssearch":
            query_dat = SELECTQUERY + f" WHERE tags = 'is_js'"
            query_count = COUNTQUERY + f" WHERE tags = 'is_js'"

    if not filedownload:
        query_dat = query_dat + " LIMIT %s OFFSET %s" % (per_page, offset)

    cur.execute(query_dat)
    data = cur.fetchall()
    
    cur.execute(query_count)
    count = cur.fetchone()

    if len(data) == 0:
        if sidemenu == "fileparses":
            return NORESULT.format(3)
        else:
            return NORESULT.format(4)

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
        return render_template('file_results.html', datas=file_fining(data), count=count[0])
    else:
        return render_template('default_results.html', datas=data_fining(data), count=count[0])

@search.route('/<sidemenu>/result', methods=['GET'])
def result(sidemenu):
    # 검색 후 페이지 로드
    tag = request.args.get('tag', '')
    menu = request.args.get('menu', '')
    key = request.args.get('key', '')
    filedownload = request.args.get('filedownload', False, type=bool)

    page = int(request.args.get('page', 1))
    id = loads(unquote(request.cookies.get('topMenu')))

    per_page = 30
    offset = (page - 1) * per_page

    conn = database_connect()
    cur = conn.cursor()

    data = []
    count = [0, ]

    query_dat = ""
    query_count = ""

    if sidemenu == "fileparses":
        file_temp_table(cur, id)
        if menu and key and tag:
            query_dat = f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult WHERE {menu} LIKE %s AND filetype = '%s'" % (f'"%{key}%"', tag)
            query_count = f"SELECT count(*) FROM temp_fileresult WHERE {menu} LIKE %s AND filetype = '%s'" % (f'"%{key}%"', tag)

        elif menu and key:
            query_dat = f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult WHERE {menu} LIKE %s" % (f'"%{key}%"')
            query_count = f"SELECT count(*) FROM temp_fileresult WHERE {menu} LIKE %s" % (f'"%{key}%"')
            
        elif tag:
            query_dat = f"SELECT se, filetype, title, url, parsed_data, moddate FROM temp_fileresult WHERE filetype = '%s'" % (tag)
            query_count = f"SELECT count(*) FROM temp_fileresult WHERE filetype = '%s'" % (tag)

        cur.execute(query_dat)
        data = cur.fetchall()

    else:
        if menu and key:
            def_temp_table(cur, id)
            if sidemenu == "content":
                query_dat = SELECTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')
                query_count = COUNTQUERY + f" WHERE {menu} LIKE %s" % (f'"%{key}%"')

            elif sidemenu == "loginpage":
                query_dat = SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_login'" % (f'"%{key}%"')
                query_count = COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_login'" % (f'"%{key}%"')
            
            elif sidemenu == "adminpage":
                query_dat = SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_admin'" % (f'"%{key}%"')
                query_count = COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_admin'" % (f'"%{key}%"')

            elif sidemenu == "neednot":
                query_dat = SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_neednot'" % (f'"%{key}%"')
                query_count = COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_neednot'" % (f'"%{key}%"')

            elif sidemenu == "gitsearch":
                query_dat = SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_github'" % (f'"%{key}%"')
                query_count = COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_github'" % (f'"%{key}%"')

            elif sidemenu == "jssearch":
                query_dat = SELECTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_js'"
                query_count = COUNTQUERY + f" WHERE {menu} LIKE %s AND tags = 'is_js'"

            query_dat = query_dat + " LIMIT %s OFFSET %s" % (per_page, offset)

            cur.execute(query_dat)
            data = cur.fetchall()
        
    cur.execute(query_count)
    count = cur.fetchone()
    
    if len(data) == 0:
        if sidemenu == "fileparses":
            return NORESULT.format(3)
        else:
            return NORESULT.format(4)

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
        return render_template('file_results.html', datas=file_fining(data), count=count[0])
    else:
        return render_template('default_results.html', datas=data_fining(data), count=count[0])

@search.route('/dashboard/default', methods=['GET'])
def dashboard():
    query = 'SELECT id FROM company'
    ids = query_database(query)
    count = len(ids)

    data = []
    for i in range(count):
        id = ids[i][0]
        query = '''
            SELECT cmp.company, count(*) FROM company cmp
            JOIN conn_comp_root ccr ON cmp.id = ccr.comp_id
            JOIN conn_root_sub crs ON ccr.root_id = crs.root_id
            JOIN conn_sub_res csr ON crs.sub_id = csr.sub_id
            JOIN searchresult sr ON csr.res_id = sr.id
            WHERE ccr.comp_id = %s;
        '''
        data += query_database(query, (id, ))

        # query = '''
        #     SELECT cmp.company, count(*) FROM company cmp
        #     JOIN conn_comp_root ccr ON cmp.id = ccr.comp_id
        #     JOIN conn_root_sub crs ON ccr.root_id = crs.root_id
        #     WHERE ccr.comp_id = %s;
        # '''
        # data += query_database(query, (i+1, ))
    return jsonify(data)