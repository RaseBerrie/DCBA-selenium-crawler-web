import multiprocessing
import subprocess

import questionary
import atexit
import time

import database
import searcher

############### SETUP ###############

def grid_setup():
    jar_path = "assets/selenium-server-4.20.0.jar"
    command = ["java", "-jar", jar_path, "standalone"]
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    questionary.print("Selenium GRID Server started.", style="fg:ansiblack")

def handle_exit():
    time.sleep(0.5)
    questionary.print("Done and Dusted. Bye! 👋", style="fg:ansiblack")

def process_function(func, items, process_count):
    chunk_size = len(items) // process_count
    chunks = [items[i * chunk_size:(i + 1) * chunk_size] for i in range(process_count)]
    
    processes = []
    for chunk in chunks:
        p = multiprocessing.Process(target=worker_function, args=(func, chunk))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

def worker_function(func, items):
    for item in items:
        func(item)

def start_menu():
    result = questionary.rawselect("What do you want to do?",
    choices=[
        "Import new CSV in command line",
        "Tag files from searched database",
        "Parse some data from files",
        "Start searching",
        "No, nevermind"
    ]).ask()
    return result

def main():
    global menu_result
    menu_result = start_menu()

    while(menu_result != "No, nevermind"):
        if menu_result == "Import new CSV in command line":
            database.new_csv_list()
            menu_result = start_menu()
            continue

        elif menu_result == "Tag files from searched database":
            print("Not supported yet!")
            menu_result = start_menu()
            continue

        elif menu_result == "Parse some data from files":
            print("Not supported yet!")
            menu_result = start_menu()
            continue

        elif menu_result == "Start searching":
            google_list = database.create_task_list("Google")
            bing_list = database.create_task_list("Bing")

            questionary.print("List Handling step finished.", style="fg:ansiblack")

            print("\n[{0}] URLs in GOOGLE search list.".format(len(google_list)))
            print("[{0}] URLs in BING search list.\n".format(len(bing_list)))
            questionary.confirm("Start searching with this option?").ask()

            #google_process = multiprocessing.Process(target=process_function, args=(wrapper_google_search, google_list, 4))
            bing_process = multiprocessing.Process(target=process_function, args=(wrapper_bing_search, bing_list, 4))

            #google_process.start()
            bing_process.start()

            #google_process.join()
            bing_process.join()

            questionary.print("Process done successfully! 🥰\n", style="fg:ansiblack")
            menu_result = start_menu()
            continue

############### WRAPPER ###############

def wrapper_google_search(item):
    driver = searcher.driver_setup()
    searcher.google_search(driver, item)
    driver.quit()

def wrapper_bing_search(item):
    driver = searcher.driver_setup()
    searcher.bing_search(driver, item)
    driver.quit()

############### MAIN ###############

if __name__ == "__main__":
    atexit.register(handle_exit)

    grid_setup()
    main()