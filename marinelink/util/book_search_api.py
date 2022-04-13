import urllib.request
import json
import requests
from src.util.constant import G_BOOK_CATEGORY_TAG, G_NAVER_API_CLIENT_ID, G_NAVER_API_SECRET_KEY


def search_book_by_keyword(a_keyword):
    """

    :param a_keyword:
    :return: List[Book]
    Book : {
        title: str, 도서 제목
        link: str, 도서 정보 링크
        image: str, 도서 이미지 링크
        author: str, 저자
        price: str, 도서 가격
        discount: str, 도서 할인 가격
        publisher: str, 도서 출판사
        pubdate: str, 도서 출판일
        isbn: str, isbn코드 (10자리 13자리)
        description: str, 도서 요약내용
        category: str, 도서 분류 항목
    }
    """
    encText = urllib.parse.quote(a_keyword)
    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", G_NAVER_API_CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", G_NAVER_API_SECRET_KEY)
    response = urllib.request.urlopen(request)

    if response.getcode() == 200:
        response_body = response.read()
        body_text = response_body.decode('utf-8')
        body_json = json.loads(body_text)
        book_list = body_json['items']
        book_list = [{**book, 'category': extract_book_category(book['link'])} for book in book_list]
        return book_list
    else:
        return []

def extract_book_category(a_url):
    s_response = requests.get(a_url)
    if s_response.status_code == 200:
        try:
            s_category = s_response.content.decode('utf-8').split(G_BOOK_CATEGORY_TAG)[1].split('>')[1].split('<')[0]
        except:
            s_category = 'unknown'
    else:
        s_category  = 'unknown'
    return s_category




