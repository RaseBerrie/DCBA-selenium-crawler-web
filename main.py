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
    with multiprocessing.Pool(process_count) as pool:
        pool.map(func, items)

def main():
    new_csv = questionary.confirm("Import new URL list?").ask()
    if new_csv:
        database.new_csv_list()

    google_list = database.create_task_list("Google")
    bing_list = database.create_task_list("Bing")

    questionary.print("List Handling step finished.", style="fg:ansiblack")
    questionary.press_any_key_to_continue().ask()

    google_process = multiprocessing.Process(target=process_function, args=(wrapper_google_search, google_list, 2))
    bing_process = multiprocessing.Process(target=process_function, args=(wrapper_bing_search, bing_list, 4))

    google_process.start()
    bing_process.start()

    google_process.join()
    bing_process.join()

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