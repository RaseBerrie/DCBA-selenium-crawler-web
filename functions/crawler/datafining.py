import pymysql
import re

def generate_regex_patterns(input_string):
    patterns = []
    length = len(input_string)
    for i in range(length):
        for j in range(i + 2, length + 1):
            patterns.append(input_string[i:j])
    return "|".join(patterns)

def git_data_fining():
    with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
        with conn.cursor() as cur:
            query = '''
                    SELECT rd.root_url, lc.company, sr.title, sr.content, sr.id
                    FROM conn_comp_root ccr
                    JOIN conn_root_sub crs ON ccr.root_id = crs.root_id
                    JOIN conn_sub_res csr ON crs.sub_id = csr.sub_id
                    JOIN search_result sr ON csr.res_id = sr.id
                    JOIN list_company lc ON ccr.comp_id = lc.id
                    JOIN domain_root rd ON ccr.root_id = rd.id
                    WHERE tags = 'is_github'
                    UNION
                    SELECT rd.root_url, lc.company, sr.title, sr.content, sr.id
                    FROM conn_comp_root ccr
                    JOIN conn_root_res crr ON ccr.root_id = crr.root_id
                    JOIN search_result sr ON crr.res_id = sr.id
                    JOIN list_company lc ON ccr.comp_id = lc.id
                    JOIN domain_root rd ON ccr.root_id = rd.id
                    WHERE tags = 'is_github';
                    '''
            cur.execute(query)
            datas = cur.fetchall()
    
    keys = []
    for data in datas:
        key = ""
        key += data[0].split(".")[0] + "|"
        key += generate_regex_patterns(data[1])

        target = data[2] + data[3]
        l = re.search(key, target)
        if l is not None:
            keys.append(str(data[4]))

    with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
        with conn.cursor() as cur:
            query = 'DELETE FROM search_result WHERE tags="is_github" AND id NOT IN ({0})'.format(",".join(keys))
            cur.execute(query)
        conn.commit()
    return 0