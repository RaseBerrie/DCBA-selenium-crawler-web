import pymysql

def query_database(query, args=(), one=False):
    conn = pymysql.connect(host='192.168.6.90',
                           user='root',
                           password='root',
                           db='searchdb',
                           charset='utf8mb4') 
    cur = conn.cursor()
    cur.execute(query, args)

    r = cur.fetchall()
    cur.close()
    conn.close()

    return (r[0] if r else None) if one else r

def database_connect():
    conn = pymysql.connect(host='192.168.6.90',
                           user='root',
                           password='root',
                           db='searchdb',
                           charset='utf8mb4')
    return conn

def def_temp_table(cur, id):
    if id["comp"][0] == 0:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_searchresult AS
                            SELECT se, subdomain, title, url, content, tags
                            FROM searchresult;'''
        cur.execute(temp_table_query)
    elif id["root"][0] == 0:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_searchresult AS
                            SELECT sr.se, sr.subdomain, sr.title, sr.url, sr.content, sr.tags
                            FROM conn_comp_root ccr
                            JOIN conn_root_sub crs ON ccr.root_id = crs.root_id
                            JOIN conn_sub_res csr ON crs.sub_id = csr.sub_id
                            JOIN searchresult sr ON csr.res_id = sr.id
                            WHERE ccr.comp_id = %s
                            UNION
                            SELECT sr.se, sr.subdomain, sr.title, sr.url, sr.content, sr.tags
                            FROM conn_comp_root ccr
                            JOIN conn_root_res crr ON ccr.root_id = crr.root_id
                            JOIN searchresult sr ON crr.res_id = sr.id
                            WHERE ccr.comp_id = %s;'''
        cur.execute(temp_table_query, (id["comp"][0], id["comp"][0], ))
    elif id["sub"][0] == 0:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_searchresult AS
                            SELECT sr.se, sr.subdomain, sr.title, sr.url, sr.content, sr.tags
                            FROM conn_root_sub crs
                            JOIN conn_sub_res csr ON crs.sub_id = csr.sub_id
                            JOIN searchresult sr ON csr.res_id = sr.id
                            WHERE crs.root_id = %s
                            UNION
                            SELECT sr.se, sr.subdomain, sr.title, sr.url, sr.content, sr.tags
                            FROM conn_root_res crr
                            JOIN searchresult sr ON crr.res_id = sr.id
                            WHERE crr.root_id = %s;'''
        cur.execute(temp_table_query, (id["root"][0], id["root"][0],))
    else:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_searchresult AS
                            SELECT sr.se, sr.subdomain, sr.title, sr.url, sr.content, sr.tags
                            FROM conn_sub_res csr
                            JOIN searchresult sr ON csr.res_id = sr.id
                            WHERE csr.sub_id = %s;'''
        cur.execute(temp_table_query, (id["sub"][0],))

def file_temp_table(cur, id):
    if id["comp"][0] == 0:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_fileresult
                            AS SELECT fl.*, sr.se FROM filelist fl
                            JOIN searchresult sr ON sr.id = fl.id
                            ORDER BY fl.moddate DESC;'''
        cur.execute(temp_table_query)
    elif id["root"][0] == 0:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_fileresult AS SELECT fl.*, sr.se
                            FROM conn_comp_root ccr
                            JOIN conn_root_sub crs ON ccr.root_id = crs.root_id
                            JOIN conn_sub_res csr ON crs.sub_id = csr.sub_id
                            JOIN filelist fl ON csr.res_id = fl.id
                            JOIN searchresult sr ON sr.id = fl.id
                            WHERE ccr.comp_id = %s
                            ORDER BY fl.moddate DESC;'''
        cur.execute(temp_table_query, (id["comp"][0],))
    elif id["sub"][0] == 0:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_fileresult SELECT fl.*, sr.se
                            FROM conn_root_sub crs
                            JOIN conn_sub_res csr ON crs.sub_id = csr.sub_id
                            JOIN filelist fl ON csr.res_id = fl.id
                            JOIN searchresult sr ON sr.id = fl.id
                            WHERE crs.root_id = %s
                            ORDER BY fl.moddate DESC;
                            '''
        cur.execute(temp_table_query, (id["root"][0],))
    else:
        temp_table_query =  '''CREATE TEMPORARY TABLE temp_fileresult SELECT fl.*, sr.se
                            FROM conn_sub_res csr
                            JOIN filelist fl ON csr.res_id = fl.id
                            JOIN searchresult sr ON sr.id = fl.id   
                            WHERE csr.sub_id = %s
                            ORDER BY fl.moddate DESC;
                            '''
        cur.execute(temp_table_query, (id["sub"][0],))

def data_fining(data):
    result = []
    for line in data:
        tmp = []
        if line[0] == "G": tmp.append("Google")
        elif line[0] == "B": tmp.append("Bing")

        if ":" in line[1]:
            str = line[1].split(':')[0]
            tmp.append(str)
        else: tmp.append(line[1])

        for i in range(2, 5): tmp.append(line[i])
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