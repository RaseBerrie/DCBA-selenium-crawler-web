import pymysql

# filter_public 태그가 달렸으면 필터링 당하는 대상
FILTER_STATUS = ' AND FIND_IN_SET("public", tags) < 1'
CREATE_DEF_TABLE = 'CREATE TEMPORARY TABLE temp_searchresult SELECT data.* FROM res_data data'
CREATE_FILE_TABLE = 'CREATE TEMPORARY TABLE temp_fileresult SELECT searchengine as se, t_file.*, data.subdomain FROM res_data data JOIN res_tags_file t_file ON t_file.url = data.res_url'

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
        temp_table_query =  CREATE_DEF_TABLE + f' WHERE FIND_IN_SET("git", tags) {find_in_set} 1 AND FIND_IN_SET("file", tags) = 0' + filter_public

    elif id["root"][0] == 0:
        temp_table_query =  CREATE_DEF_TABLE + f'''
        JOIN list_subdomain sub ON sub.url = data.subdomain
        JOIN list_rootdomain root ON root.url = sub.rootdomain
        JOIN list_company comp ON comp.company = root.company
        WHERE FIND_IN_SET("git", tags) {find_in_set} 1
        AND comp.id = {id["comp"][0]}
        ''' + filter_public

    elif id["sub"][0] == 0:
        temp_table_query =  CREATE_DEF_TABLE + f'''
        JOIN list_subdomain sub ON sub.url = data.subdomain
        JOIN list_rootdomain root ON root.url = sub.rootdomain
        WHERE FIND_IN_SET("git", tags) {find_in_set} 1
        AND root.id = {id["root"][0]}
        ''' + filter_public

    else:
        temp_table_query =  CREATE_DEF_TABLE + f'''
        JOIN list_subdomain sub ON sub.url = data.subdomain
        WHERE FIND_IN_SET("git", tags) {find_in_set} 1
        AND sub.id = {id["sub"][0]}
        ''' + filter_public

    cur.execute(temp_table_query)
        
def file_temp_table(cur, id, status):
    filter_public = ""
    if status: filter_public = FILTER_STATUS

    if id["comp"][0] == 0:
        temp_table_query =  CREATE_FILE_TABLE + '''
        WHERE 1=1''' + filter_public

    elif id["root"][0] == 0:
        temp_table_query =  CREATE_FILE_TABLE + f'''
        JOIN list_subdomain sub ON sub.url = data.subdomain
        JOIN list_rootdomain root ON root.url = sub.rootdomain
        JOIN list_company comp ON comp.company = root.company
        AND comp.id = {id["comp"][0]}
        ''' + filter_public

    elif id["sub"][0] == 0:
        temp_table_query =  CREATE_FILE_TABLE + f'''
        JOIN list_subdomain sub ON sub.url = data.subdomain
        JOIN list_rootdomain root ON root.url = sub.rootdomain
        AND root.id = {id["root"][0]}
        ''' + filter_public

    else:
        temp_table_query =  CREATE_FILE_TABLE + f'''
        JOIN list_subdomain sub ON sub.url = data.subdomain
        AND sub.id = {id["sub"][0]}''' + filter_public 

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
        
        tmp.append(line[1])
        tmp.append(line[2].upper())
        
        for i in range(3, 5): tmp.append(line[i])
        if line[6] and line[5]:
            tmp.append(line[6].strftime("%Y-%m-%d") + ", " + str(line[4]))
        elif line[5]:
            tmp.append(line[5])
        elif line[6]:
            tmp.append(line[6].strftime("%Y-%m-%d"))
        else:
            tmp.append("None")
            
        result.append(tmp)
    return result