### Importion
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from multiprocessing import Process

import random
import pymysql
import csv
import time

PAUSE_SEC = random.randrange(1,3)

### Driver setting
def driverSetup():
  options = webdriver.ChromeOptions()
  # options.add_argument('headless')
  options.add_argument('window-size=1920x1080')
  options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
  options.add_argument("--disable-blink-features=AutomationControlled")
  
  driver = webdriver.Remote(
    command_executor = 'http://127.0.0.1:4444/wd/hub',
    options = options)
  
  return driver


### Scroller
def scrolltoEndChrome(driver):
  last_height = driver.execute_script("return document.body.scrollHeight")

  while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(PAUSE_SEC)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
      try:
        time.sleep(PAUSE_SEC)
        driver.find_element(By.CLASS_NAME, "RVQdVd").click()
      except:
        break
    last_height = new_height


def scrolltoEnd(driver):
  last_height = driver.execute_script("return document.body.scrollHeight")

  while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(PAUSE_SEC)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
      break
    last_height = new_height


### GOOGLE Searcher
def googleSearch(driver, url, cur):
  searchkey = "site:" + url
  driver.get("https://www.google.com/")

  time.sleep(PAUSE_SEC)
  searchfield = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')

  searchfield.send_keys(searchkey)
  time.sleep(PAUSE_SEC)
  searchfield.send_keys(Keys.ENTER)
  
  scrolltoEndChrome(driver)
  time.sleep(PAUSE_SEC)
  resultfield = driver.find_element(By.ID, 'search')

  try:
    res_title = resultfield.find_elements(By.TAG_NAME, 'h3')
    res_link = resultfield.find_elements(By.TAG_NAME, 'cite')

    idx = len(res_title)
    for i in range(idx):
      res_title_alt = res_title[i].text
      res_title_alt = res_title_alt.replace("'", "\\'")

      query = "INSERT INTO searchresult VALUES('{0}', '{1}', '{2}', '{3}')".format("Google", url, res_title_alt, res_link[i*2].text)
      cur.execute(query)

  except Exception as e:
    print("ERROR:", e)

  resultfield = driver.find_element(By.ID, 'botstuff')
  try:
    res_title = resultfield.find_elements(By.TAG_NAME, 'h3')
    res_link = resultfield.find_elements(By.TAG_NAME, 'cite')

    idx = len(res_title)-2 # <h3 aria_hidden="true">, <h3>다시 시도</h3>
    for i in range(idx):
      res_title_alt = res_title[i].text
      res_title_alt = res_title_alt.replace("'", "\\'")

      query = "INSERT INTO searchresult VALUES('{0}', '{1}', '{2}', '{3}')".format("Google", url, res_title_alt, res_link[i*2].text)
      cur.execute(query)

  except Exception as e:
    print("ERROR:", e)

  print("Searching [{0}] from GOOGLE Done.".format(url))
  

### BING Searcher
def bingSearch(driver, url, cur):
  searchkey = "site:" + url
  driver.get("https://www.bing.com/")

  time.sleep(PAUSE_SEC)
  searchfield = driver.find_element(By.XPATH, '//*[@id="sb_form_q"]')

  searchfield.send_keys(searchkey)
  time.sleep(PAUSE_SEC)
  searchfield.send_keys(Keys.ENTER)
  
  while True:
    scrolltoEnd(driver)
    time.sleep(PAUSE_SEC)

    resultfield = driver.find_element(By.ID, 'b_results')
    try:
      res_title = resultfield.find_elements(By.TAG_NAME, 'h2')
      res_link = resultfield.find_elements(By.TAG_NAME, 'cite')

      idx = len(res_title)
      for i in range(idx):
        res_title_alt = res_title[i].text
        res_title_alt = res_title_alt.replace("'", "\\'")

        query = "INSERT INTO searchresult VALUES('{0}', '{1}', '{2}', '{3}')".format("Bing", url, res_title_alt, res_link[i].text)
        cur.execute(query)

    except Exception as e:
      print("ERROR:", e)

    try:
      time.sleep(PAUSE_SEC)
      next_page = driver.find_element(By.CLASS_NAME, 'sw_next')
      next_page.find_element(By.XPATH, '..').click()
    except:
      break

  print("Searching [{0}] from BING Done.".format(url))


### Run crawler
def runCrawler(url_list):
  ### Driver connect
  driver = driverSetup()
  conn = pymysql.connect(host='127.0.0.1', user='root',
                         password='root', db='searchdb', charset='utf8')
  cur = conn.cursor()

  ### Search
  index = 1
  for url in url_list:
    print("[{0}]".format(index), end=' ')
    googleSearch(driver, url, cur)

    print("[{0}]".format(index), end=' ')
    bingSearch(driver, url, cur)

    conn.commit()
    index = index + 1


### Main
def main():
  ### DB connect
  conn = pymysql.connect(host='127.0.0.1', user='root',
                         password='root', db='searchdb', charset='utf8')
  cur = conn.cursor()

  cur.execute("DROP TABLE IF EXISTS searchResult")
  cur.execute("CREATE TABLE searchResult (se CHAR(6), index_url CHAR(30), title VARCHAR(100), location VARCHAR(100))")

  ### Read list
  url_list = []
  with open('url_list.csv', 'r') as file:
    reader = csv.reader(file)

    for line in reader:
      url_list.append(line[0])

  ### Multiprocess
  processes = []

  n = 16
  jobs = [url_list[i*n : (i+1)*n] for i in range((len(url_list) - 1 + n) // n)]

  for job in jobs:
    p = Process(target = runCrawler, args = (job, ))
    processes.append(p)
    p.start()

  for p in processes:
    p.join()
  
  conn.close()


if __name__ == "__main__":
  main()
