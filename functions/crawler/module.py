### IMPORT
from functions.crawler.standalone import worker_function
from functions.crawler.database import create_task_list
from multiprocessing import Process

import functions.crawler.standalone as stal
import json, signal

def process_function(func, items, process_count):
    if (len(items) % process_count) == 0:
        chunk_size = (len(items) // process_count)
    else:
        chunk_size = (len(items) // process_count) + 1
    chunks = [items[i * chunk_size:(i + 1) * chunk_size] for i in range(process_count)]
    
    flag = True
    processes = []
    for chunk in chunks:
        if flag:
            p = Process(target=worker_function, args=(func, chunk))
            processes.append(p)
            p.start()        
        if len(processes) == process_count:
            flag = False

    def terminate_children():
        for p in processes:
            p.terminate()
            p.join()

    def signal_handler():
        terminate_children()
        raise SystemExit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

def process_start(json_data):
    args = json.loads(json_data)
    
    def start_searcher(key):
        if args[key]:
            ls = create_task_list(key)
            if key == "google":
                p = Process(target=process_function, args=(stal.wrapper_google_search, ls, 2))
            elif key == "github_google":
                p = Process(target=process_function, args=(stal.wrapper_google_search_github, ls, 2))
            elif key == "bing":
                p = Process(target=process_function, args=(stal.wrapper_bing_search, ls, 2))
            elif key == "github_bing":
                p = Process(target=process_function, args=(stal.wrapper_bing_search_github, ls, 2))
            p.start()

        return 0

    for key in args.keys():
        start_searcher(key)

    return 0