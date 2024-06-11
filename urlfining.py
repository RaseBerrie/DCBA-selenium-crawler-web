import pymysql

# 1. 저장된 링크를 한 줄씩 불러옴
# 2. 포트 번호 삭제
# 3. 데이터베이스에 없다면 저장
# 4. 루트 도메인이라면 그렇다고 표시 (아니라면 Default 값으로)
# 5. 해당되는 루트 도메인과 연결

def url_fining():
    with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
        with conn.cursor() as cur:
            cur.execute("select distinct searchresult.subdomain from searchresult")
            data = cur.fetchone()

    for line in data:
        print(line)

'''
if ":" in line:
    tmp = line.split(":")
    line = tmp[0] #포트 번호 삭제

found = 0
tmp = line.split(".")
if tmp.count('com') == 1:
    found = tmp.index('com')
    found = found - 1
eilf tmp.count('co') == 1 && tmp.count('kr') == 1:
    found = tmp.index('co')
    found = found - 1

'''