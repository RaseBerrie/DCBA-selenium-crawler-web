from urllib import parse
from datetime import datetime, timedelta

import pymysql
import pdfplumber
import requests
import io
import re

def parse_date(date):
    match = re.match(r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})?([+-]\d{2})'(\d{2})'?", date)
    if not match:
        raise ValueError("Invalid Date format")
    
    year, month, day, hour, minute, sec, offset_hours, offset_minutes = match.groups()
    dt = datetime(int(year), int(month), int(day), int(hour), int(minute))
    
    offset = int(offset_hours) * 60 + int(offset_minutes)
    if offset_hours[0] == '-':
        offset = -offset
    
    dt_utc = dt - timedelta(minutes=offset)
    formatted_date = dt_utc.strftime('%Y-%m-%d')
    
    formatted_date = re.sub(r'\+0000$', '+0', formatted_date)
    return formatted_date

def pdf_settitle(cur):
    cur.execute("SELECT url FROM list_file WHERE title is null or title = '' or title = 'notitle' or title = 'untitled' or title like '%무제%'")
    datas = cur.fetchall()

    for data in datas:
        url = data[0]

        date, title = find_pdf_metadata(url)
        if title == "":
            pretitle = url.split("/")[-1]

            pretitle = pretitle.replace("\\", "") #백슬래시 삭제
            pretitle = parse.unquote(pretitle) #URL 인코딩 해제
            
            if "filename=" in pretitle:
                title = pretitle.split("filename=", 1)[1]
            else:
                title = pretitle

            if "_" in title:
                title = title.split("_", 1)[1]

        query = f'UPDATE list_file SET title = "%s" WHERE url = "%s";' % (title.replace("+", " "), url)

        try:
            cur.execute(query)
        except Exception as e:
            print(e)
            print(query)
            continue

        if date:
            query = f'UPDATE list_file SET moddate = %s WHERE url = "%s";' % (date, url)
            try:
                cur.execute(query)
            except Exception as e:
                print(e)
                print(query)
                continue

def find_pdf_metadata(url):
    response = requests.get(url)
    pdf_buffer = io.BytesIO(response.content)
    pdf = pdfplumber.open(pdf_buffer)

    metadata = pdf.metadata
    date = metadata["ModDate"]
    title = metadata["Title"]

    return parse_date(date), title

def find_sublist(nested_list, target):
    # 재귀적으로 모든 단계의 중첩 리스트를 탐색
    for item in nested_list:
        if isinstance(item, list):
            sublist_result = find_sublist(item, target)
            if sublist_result is not None:
                return sublist_result
        elif isinstance(item, str) and target in item:
            return nested_list
    return None

def pdf_parse_search(url, keyword):
    response = requests.get(url)
    
    pdf_buffer = io.BytesIO(response.content)
    pdf = pdfplumber.open(pdf_buffer)

    page_result = ""
    pages = pdf.pages
    for page in pages:
        tables = page.extract_tables()
        if tables:
            result = find_sublist(tables, keyword)
            if result:
                result = [i for i in result if i]
                result_string = ", ".join(result)
                page_result = page_result + result_string

    if page_result:
        page_result = page_result.replace("\n", " ")
    else:
        page_result = "No result"
    return page_result

########################## 코드영역 ##########################

with pymysql.connect(host='192.168.6.90', user='root', password='root', db='searchdb', charset='utf8mb4') as conn:
    with conn.cursor() as cur:
        # query = "select url, id from list_file where filetype = 'pdf' and moddate is null"
        # cur.execute(query)

        # datas = cur.fetchall()
        # for data in datas:
        #     url = data[0]
        #     try:
        #         date, title = find_pdf_metadata(url)
        #         query = f"update list_file set moddate = '%s' where id = %d" % (date, data[1])
        #         cur.execute(query)
                
        #         query = f"update list_file set title = '%s' where id = %d" % (title, data[1])
        #         cur.execute(query)
        #         conn.commit()

        #         print(str(date) + ", " + title)
        #     except:
        #         continue
        pdf_settitle(cur)
        conn.commit()