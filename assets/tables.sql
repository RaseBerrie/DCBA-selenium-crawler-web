### 검색 결과 테이블
CREATE TABLE searchResult (id INT AUTO_INCREMENT PRIMARY KEY,
                           search_key CHAR(30) not null,
                           title VARCHAR(100) not null,
                           url VARCHAR(500) not null,
                           content text);

### 검색 키(작업 완료 URL 리스트)테이블
CREATE TABLE IF NOT EXISTS searchKeys (search_key CHAR(30) NOT NULL UNIQUE,
                                       google CHAR(1) NOT NULL DEFAULT "N",
                                       bing CHAR(1) NOT NULL DEFAULT "N");

### 태그 테이블
CREATE TABLE IF NOT EXISTS searchTags (id INT AUTO_INCREMENT PRIMARY KEY,
                                       tag VARCHAR(255) UNIQUE);