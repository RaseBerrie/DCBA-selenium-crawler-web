import pymysql

# 1. 저장된 링크를 한 줄씩 불러옴
# 2. 포트 번호 삭제
# 3. 데이터베이스에 없다면 저장
# 4. 루트 도메인이라면 그렇다고 표시 (아니라면 Default 값으로)
# 5. 해당되는 루트 도메인과 연결

def url_fining():
    with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT searchresult.subdomain FROM searchresult")
            datas = cur.fetchall()

    notfoundcount = 0
    s = set()
    for data in datas:
        line = data[0]
        print("DATA: " + line)

        if ":" in line:
            tmp = line.split(":")
            line = tmp[0] # 포트 번호 삭제

        found = 0
        tmp = line.split(".")

        # tmp에서 com이 나오는 인덱스 번호를 found에 저장함
        if tmp.count('com') == 1:
            found = tmp.index('com')
            found = found - 1

            tmplist = tmp[found:]
            tmpstr = ".".join(tmplist)
            print("FINED: " + tmpstr + "\n")
            s.add(tmpstr)
        elif ((tmp.count('co') == 1) and (tmp.count('kr') == 1)):
            found = tmp.index('co')
            found = found - 1

            tmplist = tmp[found:]
            tmpstr = ".".join(tmplist)
            print("FINED: " + tmpstr + "\n")            
            s.add(tmpstr)
        elif tmp.count('jp') == 1:
            found = tmp.index('jp')
            found = found - 1

            tmplist = tmp[found:]
            tmpstr = ".".join(tmplist)
            print("FINED: " + tmpstr + "\n")
            s.add(tmpstr)
        else:
            print("[### FAILED ###]\n")
            notfoundcount = notfoundcount + 1

    print("================================\n")
    print("TOTAL: " + str(len(datas)))
    print("FINED: " + str(len(s)))
    print("FAILED: " + str(notfoundcount))

    for line in s:
        with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT IGNORE INTO rootdomain(root_url) VALUES('{0}')".format(line))
            conn.commit()
    
    return 0

def url_connecting():
    conn = pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("SELECT * FROM rootdomain")
    datas = cur.fetchall()
    
    for data in datas:
        r_id = data[0]
        r_val = data[1]

        query = "SELECT id FROM searchresult WHERE subdomain LIKE '%{0}%'".format(r_val)
        cur.execute(query)
        ids = cur.fetchall()

        for id in ids:
            sub_id = id[0]
            query = "INSERT IGNORE INTO conn_domain_result(root_domain_id, search_url_id) VALUES({0}, {1})".format(r_id, sub_id)
            cur.execute(query)

        conn.commit()
    
    cur.close()
    conn.close()
    
    return 0