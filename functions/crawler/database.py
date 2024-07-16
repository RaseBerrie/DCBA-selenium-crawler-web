import questionary
import pymysql
import csv
import time

def new_csv_list():
    time.sleep(0.5)
    newcsv = questionary.path("Please select your CSV file.").ask()
    while '.csv' not in newcsv:
        questionary.print("This is not a proper CSV file 😢", style="fg:ansiblack")
        newcsv = questionary.path("Please select your CSV file.").ask()

    url_list = []
    with open(newcsv, 'r') as file:
        reader = csv.reader(file)    
        for line in reader:
            url_list.append(line[0])

    try:
        with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
            with conn.cursor() as cur:
                query = '''
                CREATE TABLE IF NOT EXISTS searchKeys (
                    search_key CHAR(30) not null unique,
                    Google CHAR(1) not null default "N",
                    Bing CHAR(1) not null default "N")
                '''
                cur.execute(query)
                for url in url_list:                 
                    cur.execute("INSERT IGNORE INTO searchKeys(search_key) VALUES('{0}')".format(url))   
            conn.commit()

    except Exception as e:
        print(e)

def create_task_list(task):
    result = []
    with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
        with conn.cursor() as cur:
            url = cur.execute("SELECT search_key FROM searchKeys WHERE {0}='N'".format(task))
            while url:
                if str(type(url)) == "<class 'tuple'>":
                    result.append(url[0])
                url = cur.fetchone()

    return result