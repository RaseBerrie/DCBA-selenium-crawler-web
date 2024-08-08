import multiprocessing, subprocess
import questionary, atexit, time
try:
    from functions.crawler import database, searcher, urlfining, dbbuilder
except:
    import database, searcher, urlfining, dbbuilder


############### SETUP ###############

def grid_setup():
    jar_path = "assets/selenium-server-4.20.0.jar"
    command = ["java", "-jar", jar_path, "standalone"]
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    questionary.print("Selenium GRID Server started.", style="fg:ansiblack")
    return 0

def handle_exit():
    time.sleep(0.5)
    questionary.print("Done and Dusted. Bye! 👋", style="fg:ansiblack")
    return 0

def process_function(func, items, process_count):
    if (len(items) % process_count) == 0: chunk_size = (len(items) // process_count)
    else: chunk_size = (len(items) // process_count) + 1
        
    chunks = [items[i * chunk_size:(i + 1) * chunk_size] for i in range(process_count)]
    
    flag = True
    processes = []
    for chunk in chunks:
        if flag:
            p = multiprocessing.Process(target=worker_function, args=(func, chunk))
            processes.append(p)
            p.start()

        if len(processes) == process_count:
            flag = False

    for p in processes: p.join()
    return 0

def worker_function(func, items):
    for item in items: func(item)
    return 0

def start_menu():
    result = questionary.rawselect("What do you want to do?",
    choices=[
        "EXIT! 🛸",
        "Import new CSV in command line",
        "Find ROOT URLs from search results",
        "Find SUBDOMAINs and make connections",
        "Start searching",
    ]).ask()
    return result

def main():
    global menu_result
    menu_result = start_menu()

    while(menu_result != "EXIT! 🛸"):
        if menu_result == "Import new CSV in command line":
            database.new_csv_list()
            menu_result = start_menu()
            continue

        elif menu_result == "Find ROOT URLs from search results":
            urlfining.url_fining()
            questionary.print("Process done successfully! 🥰\n", style="fg:ansiblack")

            menu_result = start_menu()
            continue

        elif menu_result == "Find SUBDOMAINs and make connections":
            dbbuilder.dbbuild()
            dbbuilder.dbbuild_root()

            questionary.print("Process done successfully! 🥰\n", style="fg:ansiblack")

            menu_result = start_menu()
            continue

        elif menu_result == "Start searching":
            google_list = database.create_task_list("Google")
            bing_list = database.create_task_list("Bing")

            google_list_line = "GOOGLE: [{0}] URLs".format(len(google_list))
            bing_list_line = "BING: [{0}] URLs".format(len(bing_list))

            questionary.print("List Handling step finished.", style="fg:ansiblack")
            select = questionary.checkbox("Select list(s) to search.",
                                          choices=[google_list_line, bing_list_line]).ask()

            confirm = questionary.confirm("Start searching with this option?").ask()

            if confirm:
                if google_list_line in select and bing_list_line in select:
                    google_process = multiprocessing.Process(target=process_function, args=(wrapper_google_search, google_list, 4))
                    bing_process = multiprocessing.Process(target=process_function, args=(wrapper_bing_search, bing_list, 4))

                    google_process.start()
                    bing_process.start()

                    google_process.join()
                    bing_process.join()

                elif google_list_line in select:
                    google_process = multiprocessing.Process(target=process_function, args=(wrapper_google_search, google_list, 4))
                    google_process.start()
                    google_process.join()
                
                else:
                    bing_process = multiprocessing.Process(target=process_function, args=(wrapper_bing_search, bing_list, 4))
                    bing_process.start()
                    bing_process.join()

                questionary.print("Process done successfully! 🥰\n", style="fg:ansiblack")

            menu_result = start_menu()
            continue

    return 0


############### WRAPPER ###############

def wrapper_search(engine, item, is_git):
    if engine == 'google':
        if is_git: searcher.google_search(item, "github")
        else: searcher.google_search(item)
    elif engine == 'bing':
        if is_git: searcher.bing_search(item, "github")
        else: searcher.bing_search(item)

def wrapper_google_search(item):
    wrapper_search('google', item, False)

def wrapper_bing_search(item):
    wrapper_search('bing', item, False)

def wrapper_google_search_github(item):
    wrapper_search('google', item, True)

def wrapper_bing_search_github(item):
    wrapper_search('bing', item, True)

############### MAIN ###############

if __name__ == "__main__":
    atexit.register(handle_exit)

    grid_setup()
    main()