import pymysql
try:
    from functions.crawler.urlfining import url_fining
except:
    from urlfining import url_fining

############### DEF ###############
def insert_into_subdomain(cur):
    cur.execute("SELECT DISTINCT search_result.subdomain FROM search_result")
    datas = cur.fetchall()

    for data in datas:
        line = data[0]
        if ":" in line:
            tmp = line.split(":")
            line = tmp[0] # 포트 번호 삭제
        cur.execute("INSERT IGNORE INTO domain_sub(sub_url) VALUES('{0}')".format(line))    

def delete_from_subdomain(cur):
    cur.execute("SELECT root_url FROM domain_root")
    datas = cur.fetchall()

    for data in datas:
        root_url = data[0]
        cur.execute("DELETE FROM domain_sub WHERE sub_url LIKE '{0}'".format(root_url))

def insert_from_key_to_subdomain(cur):
    cur.execute("SELECT search_key FROM search_key")
    keys = cur.fetchall()

    for key in keys:
        subdomain = key[0]
        cur.execute("INSERT IGNORE INTO domain_sub(sub_url) VALUES('{0}')".format(subdomain))

def conn_sub_res(cur):
    cur.execute("SELECT * FROM domain_sub")
    suburls = cur.fetchall()

    for suburl in suburls:
        url = suburl[1]
        cur.execute("SELECT id FROM search_result WHERE subdomain LIKE '{0}%'".format(url))
        ids = cur.fetchall()

        for id in ids:
            cur.execute("INSERT ignore INTO conn_sub_res(sub_id, res_id) VALUES({0}, {1})".format(suburl[0], id[0]))
            
def conn_root_sub(cur):
    cur.execute("SELECT * FROM domain_root")
    datas = cur.fetchall()

    for data in datas:
        root_url = data[1]
        cur.execute("SELECT id FROM domain_sub WHERE sub_url LIKE '%.{0}'".format(root_url))
        ids = cur.fetchall()

        for id in ids:
            cur.execute("INSERT IGNORE INTO conn_root_sub(root_id, sub_id) VALUES ({0}, {1})".format(data[0], id[0]))

def conn_root_res(cur):
    query = '''
        SELECT sr.subdomain, sr.id FROM search_result sr
        LEFT JOIN conn_sub_res csr ON sr.id = csr.res_id
        WHERE csr.sub_id IS NULL;
    '''
    cur.execute(query)
    datas = cur.fetchall()

    for data in datas:
        root_url = data[0]
        root_url = root_url.split(":")[0]
        cur.execute("SELECT id FROM domain_root WHERE root_url='{0}'".format(root_url))

        id = cur.fetchone()
        try:
            cur.execute("INSERT IGNORE INTO conn_root_res(root_id, res_id) VALUES({0}, {1})".format(id[0], data[1]))
        except Exception as e:
            print(e)

############### FUNCTION ###############
def dbbuild():
    conn = pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4')
    cur = conn.cursor()

    insert_into_subdomain(cur)
    delete_from_subdomain(cur)
    conn_root_sub(cur)
    conn_sub_res(cur)

    conn.commit()
    cur.close()
    conn.close()

def dbbuild_root():
    conn = pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4')
    cur = conn.cursor()
    conn_root_res(cur)
    conn.commit()
    cur.close()
    conn.close()

def dbbuild_module():
    with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
        with conn.cursor() as cur:
            insert_from_key_to_subdomain(cur)
        conn.commit()

    url_fining()
    with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
        with conn.cursor() as cur:
            delete_from_subdomain(cur)
