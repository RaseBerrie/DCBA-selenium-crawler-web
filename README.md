# Selenium URL Crawling
제공된 리스트의 사이트에 대한 검색 내역을 크롤링한다. CSV 파일로 제공된 리스트(url_list.csv)를 읽어온 후 셀레니움 그리드를 이용한 원격 브라우저로 검색을 실행한다. MySQL 데이터베이스에 연결해 크롤링 결과를 저장한다.

## Dependencies
* `Selenium` 4.20.0
* `PyMySQL` 1.1.0 
* `MySQL Server` 8.0.37
* `Selenium Grid` 4.20.0
* `Flask` 3.0.3