import pdfplumber
import requests
import io

def find_sublist_containing_string(nested_list, target):
    # 재귀적으로 모든 단계의 중첩 리스트를 탐색
    for item in nested_list:
        if isinstance(item, list):
            sublist_result = find_sublist_containing_string(item, target)
            if sublist_result is not None:
                return sublist_result
        elif isinstance(item, str) and target in item:
            return nested_list
    return None

def parse_pdf_then_search(url, keyword):
    response = requests.get(url)
    
    pdf_buffer = io.BytesIO(response.content)
    pdf = pdfplumber.open(pdf_buffer)

    pages = pdf.pages
    for page in pages:
        tables = page.extract_tables()
        if tables:
            result = find_sublist_containing_string(tables, keyword)
            if result:
                result = [i for i in result if i]
                result_string = ", ".join(result)
                print(result_string)
                
parse_pdf_then_search(r'https://img.shinhan.com/sbank2016/seol/20211227000000790002LC000030.PDF', "피보험자")