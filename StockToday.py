# requests, BeautifulSoup4를 통한 웹 크롤링
# 1: 리스트 자료형, split(), replace(), datetime, 형 변환, for문, 중첩 for문, if문, format(), round()
# 2, 3: 함수


import datetime
import requests
from bs4 import BeautifulSoup


# 공통되는 네이버 검색창 url
url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="

kakao = "카카오"
samsung = "삼성전자"
microsoft = "마이크로소프트"
apple = "애플"

rate = "환율"

korea_stock = [kakao, samsung]
us_stock = [microsoft, apple]

stock = [korea_stock, us_stock]


# 정보 담아오는 함수
def bs(search):
    html = requests.get(url+search)
    soup = BeautifulSoup(html.content, "html.parser")
    searched = soup.find("span",{"class":"spt_con"}).text

    return searched


# "지수" 기준으로 금액만 추출해서 천의자리 쉼표 제거하는 함수
def money(searched):
    return searched.split("지수")[1].split(" ")[0]


# 천의자리 쉼표 넣고 float 형으로 변환하는 함수
def toFloat(money):
    return round(float(money.replace(",","")),2)


# 달러일 경우 원화로 변환하는 함수
def exchange(dollar):
    return str(format(round(dollar * toFloat(dollar_today),2),","))


# 달러일 경우 등락 금액 추출 함수
def fluctuation(s_text):
    s_fluc_list = (s_text.split("전일대비 ")[1]).split(" ")
    s_fluc = float(s_fluc_list[1])
    s_fluc_ex = str(exchange(s_fluc))
    s_fluc_str = s_fluc_list[0] + " " + s_fluc_ex

    if s_fluc_list[0] == "상승":
        return s_fluc_str + " " + s_fluc_list[2].replace("(","(+")
    elif s_fluc_list[0] == "하락":
        return s_fluc_str + " " + s_fluc_list[2].replace("(","(-").replace("--","-")
    else:
        return s_fluc_str + " " + s_fluc_list[2]


dollar_today = money(bs(rate)) # 환율 정보가 담기는 부분
now = datetime.datetime.now() # 현재시간

print(now)
print("현재 환율: "+dollar_today)
print()
print("(단위: 원)")


for list in stock:
    for s in list:
        s_text = bs(s)

        if s in us_stock: # 미국 주식일 경우
            print(s+" 지수 "+exchange(toFloat(money(s_text)))+" 전일대비 "+fluctuation(s_text))
        else: # 한국 주식일 경우
            print(s+s_text.replace("  "," ")) # 그대로 출력



"""
출력 결과:

2021-10-27 16:44:07.250573
현재 환율: 1,170.0

(단위: 원)
카카오 지수 128,500 전일대비 상승 1,000 (+0.78%) 
삼성전자 지수 70,100 전일대비 하락 1,000 (-1.41%) 
마이크로소프트 지수 362,828.7 전일대비 상승 2,316.6 (+0.64%)
애플 지수 174,704.4 전일대비 상승 795.6 (+0.46%)
"""