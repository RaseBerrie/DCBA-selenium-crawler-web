from main import *
from functions.dbconnect import query_database

import io
import os
import signal
import psutil
import time
import subprocess
import csv

from flask import Blueprint, render_template, make_response, request
crawler = Blueprint('crawler', __name__, template_folder='templates/crawler', url_prefix="/crawler")

def new_csv_list(file_storage):
    result = []
    with io.StringIO(file_storage.read().decode('utf-8-sig')) as file:
        file.seek(0)
        reader = csv.reader(file)

        for line in reader:
            result.append(line[0])
    return result

@crawler.route('/')
def crawler_page():
    pid = request.cookies.get("pid")
    query = "select * from searchkeys"
    datas = query_database(query)

    if pid: return render_template('crawler_inprocess.html', processing=False)
    else: return render_template('crawler_start.html', datas=datas)

@crawler.route('/start')
def start():
    process = subprocess.Popen(
        ["python", "functions/crawler/test.py"], 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        text=True
    )
    crawler_pid = str(process.pid)

    line = process.stdout.readline()
    if line: print(line.strip())

    resp = make_response(render_template('crawler_inprocess.html', processing=True))
    resp.set_cookie("pid", crawler_pid)

    return resp

@crawler.route('/finish')
def finish():
    pid = int(request.cookies.get("pid"))
    ISDONE = f"서브 프로그램 종료됨 (PID: {pid})"
    
    data = "result: "
    if psutil.pid_exists(pid):
        try:
            os.kill(pid, signal.SIGTERM)
            data += ISDONE
        except Exception as e:
            time.sleep(0.1)
            if psutil.pid_exists(pid):
                try:
                    os.kill(pid, signal.SIGTERM)
                    data += ISDONE
                except Exception as e: data += f"프로세스 종료 중 오류 발생: {e}"
            else: data += ISDONE
    else: data += ISDONE

    resp = make_response(data)
    resp.set_cookie("pid", "", expires=0)
    
    return resp

@crawler.route('/addlinks', methods=['GET', 'POST'])
def addlinks():
    result = {}
    
    if request.method == 'GET':
        comp = request.args.get("comp")
        data = request.args.get("data")

        result_data = data.split("\n")
        result[comp] = result_data

    else:
        comp = request.form['comp']
        data = request.files['data']

        result_data = new_csv_list(data)
        result[comp] = result_data

    return result