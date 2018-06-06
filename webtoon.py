import os
import sys
from urllib import parse

import requests
from bs4 import BeautifulSoup

from utils_webtoon import Webtoon


def search_webtoon(keyword):
    # 전체 웹툰에서 제목, titleId 가져오는 크롤링
    file_path = 'data/webtoon_list.html'
    # 파일경로: data폴더에 webtoon_list.html이라는 파일을 생성
    webtoon_url = 'http://comic.naver.com/webtoon/weekday.nhn'
    # webtoon_url 이라는 변수에 주소 할당

    if not os.path.exists(file_path):
        # 파일 존재 유무에 대해 확인하는 구문
        # 만약 파일이 존재한다면
        response = requests.get(webtoon_url)
        # 웹툰 url에 주소를 얻어 response라는 변수에 할당
        html = response.text
        # 그러한 response를 text형태로 html이라는 변수에 할당
        open(file_path, 'wt').write(html)
        # 열어서 해당 내용에 대해 덮어쓰자
    else:
        # 만약에 파일이 없다면
        html = open(file_path, 'rt').read()
        # 열어서 읽는것을 html이라는 변수에 할당
    soup = BeautifulSoup(html, 'lxml')
    # BeautifulSoup 모듈을 통해 아까 html이라는 변수에 할당한 내용의
    # 데이터를 뽑아내는 과정
    a_list = soup.select('a.title')
    # a태그에 title이라는 클래스를 가진 애들을 모두 추출하여
    # a_list라는 변수에 할당

    # 대학입력시 해당 키워드를 가지고 있는 웹툰 title와 웹툰 titleId
    result_list = []
    #
    webtoon_id_set = set()
    # webtoon_id_set이라는 변수는 반복되는 것을 막고자
    # set이라는 내장함수를 통해 걸러준 값을 할당받을 변수다
    for a in a_list:
        # 위에서 a태그에 title.이라는 내용의 변수를 반복문을 돌릴 것이다.
        href = a.get('href')
        # 그러한 것중 각각 a태그에서 href(주소)를 얻어 href에 할당
        query_string = parse.urlsplit(href).query
        # 이 구문은 지금도 잘 설명하기 까다로움
        query_dict = dict(parse.parse_qsl(query_string))
        # 위에서 추출한 내용을 딕셔너리 형태로 query_dict 변수에 할당
        webtoon_id = query_dict.get('titleId')
        # 딕셔너리에서 Id값을 얻어 webtoon_id라는 변수에 할당
        title = a.get_text(strip=True)
        # a태그를 텍스트형식으로 여백없이 추출하여 title이라는 변수에 할당
        if keyword in title:
            # 만약 title에 keyword가 있다면
            # webtoon_id가 중복되는 경우 continue
            if webtoon_id in webtoon_id_set:
                # 중복되는 것(딕셔너리형태)을 id값을 확인하기 위해
                # if문을 사용
                # print(f'중복되는 웹툰:{webtoon_id}')
                continue

            webtoon_id_set.add(webtoon_id)
            # 모든 웹툰이 뽑아져 나오면서 계속해서 더해지며
            # 나열 될 것이다.
            result_list.append({
                'webtoon_id': webtoon_id,
                'title': title,
            })
            # 추가가되는데 딕셔너리 형태로 뽑아내며
            # 웹툰의 id 값과 제목으로 나올 것이다.
    return result_list
    # 만약 keyword가 존재한다면 result_list를 리턴
def ini():
    search_keyword = input('검색할 웹툰명을 입력해주세요')
    # input을 통해 cmd창에서 나올 내용

    result_list = search_webtoon(search_keyword)
    # 입력받은 내용을 통해 search_webtoon 함수 실행
    for num, webtoon in enumerate(result_list):
        print(f'{num}: {webtoon["title"]}')
    # enumerate를 통해 순차적으로
    # ex) 0 웹툰제목1
    # ex) 1 웹툰제목2   이러한 형태로 나열할 것이다.

    select_webtoon = input("선택 :")
    # 원하는 번호 입력
    webtoon1 = Webtoon(webtoon_id=result_list[int(select_webtoon)]['webtoon_id'])
    # 위에 input함수는 str으로만 출력되지만 int내장함수를 통해 숫자로 변환
    # (왜냐하면 우리는 enumerate를 통해 0,1,2,3 숫자로 표기해줬음)
    # 그 이후는 설명을 잘 못하겠습니다.
    select_webtoon_menu(webtoon1)

def select_webtoon_menu(webtoon):
    # cmd창에 웹툰의 선택목록들이 나오는 구간
    while True:
        # break를 입력할때까지 계속 반복할 것이다.
        print('---------------------------------------------')
        # 가독성을 위해 넣어준 것
        print(f'현재 {webtoon.title} 웹툰이 선택되어 있습니다.')
        print('1. 웹툰 정보 보기')
        print('2. 웹툰 저장하기')
        print('3. 다른 웹툰 검색해서 선택하기')
        print('4. 종료하기')
        select_menu = input('선택 :')
        # 우리가 입력한 숫자를 select_menu라는 변수에 할당

        if select_menu is '1':
            print('---------------------------------------------')
            print(webtoon.show_info())
        # 만약 1번을 선택한다면 웹툰의 info들을 쭉 보여줄 것이다.
        # 여기서 info는 title과 저자, description 이다.
        elif select_menu is '2':
        # 만약 2번을 선택하면 pass
            pass
        elif select_menu is '3':
            ini()
        # 3번을 위에 매서드 재실행
        elif select_menu is '4':
            sys.exit(1)
        # 4번을 누르면 빠져나올것이다
        else:
            print('올바른 입력이 아닙니다. 다시 선택해주세요')
        # 위에서 만들어준 번호 이외 (5번부터)는 이 문장이 출력 될 것이다.

if __name__ == '__main__':
    ini()

# 이부분은 좀더 공부 필요