# requests, BeautifulSoup4를 통한 웹 크롤링
# 리스트 자료형, split(), replace(), datetime, 형 변환, for문, 중첩 for문, if문, format(), round()

import datetime
import requests
from bs4 import BeautifulSoup

# 공통되는 네이버 검색창 url
url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="

kakao = "카카오"
samsung = "삼성전자"
microsoft = "마이크로소프트"
apple = "애플"

dollar = "환율"

korea_stock = [kakao, samsung]
us_stock = [microsoft, apple]

stock = [korea_stock, us_stock]

dollar_html = requests.get(url+dollar)
dollar_soup = BeautifulSoup(dollar_html.content, "html.parser")
dollar_today = dollar_soup.find("span",{"class":"spt_con"}) # 환율 정보가 담기는 부분

d = dollar_today.text.split("지수")[1] # 환율만 추출
d_float = float(d.split(" ")[0].replace(",","")) # 천의자리 쉼표 제거 후 float 변환

now = datetime.datetime.now() # 현재시간
print(now)
print("현재 환율: "+str(d_float))

for list in stock:
    for s in list:
        html = requests.get(url+s)
        soup = BeautifulSoup(html.content, "html.parser")

        # 수정 중
        if s in us_stock: # 미국 주식일 경우
            stock_today = soup.find("span",{"class":"spt_con"}) # 주가 정보가 담기는 부분
            s_float = float(stock_today.text.split("지수")[1].split(" ")[0].replace(",","")) # 주가만 추출
            s_str = str(format(round(d_float * s_float),",")) # 환율과 곱하기 → 반올림 → 천의 자리 쉼표 삽입 → string 변환 
            print(s+"지수 "+s_str+stock_today.text.split(str(s_float))[1])
        else: # 한국 주식일 경우
            stock_today = soup.find("span",{"class":"spt_con"}) # 주가 정보가 담기는 부분
            print(s+stock_today.text) # 그대로 출력


"""
출력 결과:

2021-10-27 11:35:20.980860
현재 환율: 1168.1
카카오 지수 127,500  전일대비 보합  0 (0%)  
삼성전자 지수 70,100  전일대비 하락  1,000 (-1.41%)  
마이크로소프트지수 362,239  전일대비 상승 1.98 (0.64%)  
애플지수 174,421  전일대비 상승 0.68 (0.46%)  
"""