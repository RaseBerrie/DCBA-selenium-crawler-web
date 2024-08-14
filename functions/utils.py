import pymysql

# filter_public 태그가 달렸으면 필터링 당하는 대상
FILTER_STATUS = '''
                AND FIND_IN_SET('public', tags) < 1
                '''
CREATE_DEF_TABLE =  '''
                    CREATE TEMPORARY TABLE temp_searchresult
                    SELECT con.* FROM res_data_content con
                    '''
CREATE_FILE_TABLE = '''
                    CREATE TEMPORARY TABLE temp_fileresult
                    SELECT DISTINCT con.searchengine as se, t_file.* FROM res_data_content con
                    JOIN res_tags_file t_file ON t_file.url = con.res_url
                    '''

def database_connect():
    conn = pymysql.connect(host='192.168.6.90',
                           user='root',
                           password='root',
                           db='searchdb',
                           charset='utf8mb4')
    return conn

def database_query(query, args=(), one=False):
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(query, args)

    r = cur.fetchall()
    cur.close()
    conn.close()

    return (r[0] if r else None) if one else r

def def_temp_table(cur, id, status, git=False):
    filter_public = ''
    if status: filter_public = FILTER_STATUS

    if git: find_in_set = '>'
    else: find_in_set = '<'

    if id["comp"][0] == 0:
        temp_table_query =  CREATE_DEF_TABLE + f'WHERE FIND_IN_SET("git", tags) {find_in_set} 1' + filter_public

    elif id["root"][0] == 0:
        temp_table_query =  CREATE_DEF_TABLE + f'''
        JOIN res_data_label lab ON lab.label = con.res_url
        JOIN res_closure clo ON lab.id = clo.descendant
        WHERE FIND_IN_SET("git", tags) {find_in_set} 1
        AND ((ancestor = {id["comp"][0]} AND depth = 3)
        OR (ancestor = {id["comp"][0]} AND depth = 2 AND lab.label LIKE "http%"))
        ''' + filter_public

    elif id["sub"][0] == 0:
        temp_table_query =  CREATE_DEF_TABLE + f'''
        JOIN res_data_label lab ON lab.label = con.res_url
        JOIN res_closure clo ON lab.id = clo.descendant
        WHERE FIND_IN_SET("git", tags) {find_in_set} 1
        AND ((ancestor = {id["root"][0]} AND depth = 2)
        OR (ancestor = {id["root"][0]} AND depth = 1 AND lab.label LIKE "http%"))
        ''' + filter_public

    else:
        temp_table_query =  CREATE_DEF_TABLE + f'''
        JOIN res_data_label lab ON lab.label = con.res_url
        JOIN res_closure clo ON lab.id = clo.descendant
        WHERE FIND_IN_SET("git", tags) {find_in_set} 1
        AND ancestor = {id["sub"][0]}''' + filter_public

    cur.execute(temp_table_query)
        
def file_temp_table(cur, id, status):
    filter_public = ""
    if status: filter_public = FILTER_STATUS

    if id["comp"][0] == 0:
        temp_table_query =  CREATE_FILE_TABLE + '''
        WHERE 1=1''' + filter_public

    elif id["root"][0] == 0:
        temp_table_query =  CREATE_FILE_TABLE + f'''
        JOIN res_data_label lab ON lab.label = con.res_url
        JOIN res_closure clo ON lab.id = clo.descendant
        WHERE ((ancestor = {id["comp"][0]} AND depth = 3)
        OR (ancestor = {id["comp"][0]} AND depth = 2))
        ''' + filter_public

    elif id["sub"][0] == 0:
        temp_table_query =  CREATE_FILE_TABLE + f'''
        JOIN res_data_label lab ON lab.label = con.res_url
        JOIN res_closure clo ON lab.id = clo.descendant
        WHERE ((ancestor = {id["root"][0]} AND depth = 2)
        OR (ancestor = {id["root"][0]} AND depth = 1))
        ''' + filter_public

    else:
        temp_table_query =  CREATE_FILE_TABLE + f'''
        JOIN res_data_label lab ON lab.label = con.res_url
        JOIN res_closure clo ON lab.id = clo.descendant
        WHERE ancestor = {id["sub"][0]}''' + filter_public 

    cur.execute(temp_table_query)

def data_fining(data):
    result = []
    for line in data:
        tmp = []
        if line[1] == "G": tmp.append("Google")
        elif line[1] == "B": tmp.append("Bing")

        if ":" in line[2]:
            str = line[2].split(':')[0]
            tmp.append(str)
        else: tmp.append(line[2])

        for i in range(4, 7): tmp.append(line[i])
        result.append(tmp)
    return result

def file_fining(data):
    result = []
    for line in data:
        tmp = []

        if line[0] == "G": tmp.append("Google")
        elif line[0] == "B": tmp.append("Bing")

        tmp.append(line[1].upper())
        
        for i in range(2, 4): tmp.append(line[i])
        if line[5] and line[4]:
            tmp.append(line[5].strftime("%Y-%m-%d") + ", " + str(line[4]))
        elif line[4]:
            tmp.append(line[4])
        elif line[5]:
            tmp.append(line[5].strftime("%Y-%m-%d"))
        else:
            tmp.append("None")
        result.append(tmp)

    return result