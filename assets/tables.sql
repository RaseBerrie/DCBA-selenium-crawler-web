### 검색 결과 테이블
CREATE TABLE searchResult (
    se CHAR(1) NOT NULL,
    subdomain VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    url VARCHAR(500) NOT NULL,
    content TEXT,
    CONSTRAINT unique_se_url UNIQUE (se, url)
);

### 검색 키(작업 완료 URL 리스트)테이블
CREATE TABLE IF NOT EXISTS searchKeys (
    search_key CHAR(30) NOT NULL UNIQUE,
    google CHAR(1) NOT NULL DEFAULT "N",
    bing CHAR(1) NOT NULL DEFAULT "N"
);