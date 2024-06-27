#모듈
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import time, random
import pprint
from more_itertools import flatten

#테스
#df = pd.read_json(r'C:\Users\gwqt1\Desktop\고려대 세종\2학년\202R\텍스트마이닝(BIDS306)\텍스트마이닝_레포트\df_전체\df.json')
url ='https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=102&oid=023&aid=0003579891'
    
#네이버 뉴스 본문 ==============================================================
header = { 
    "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",      
}
   
def get_news(n_url):
    news_detail = []
    print(n_url)
    breq = requests.get(n_url, headers=header)
    bsoup = BeautifulSoup(breq.content, 'html.parser')

    # 제목 파싱
    title = bsoup.select('h3#articleTitle')[0].text
    news_detail.append(title)

    # 날짜
    pdate = bsoup.select('.t11')[0].get_text()[:11]
    news_detail.append(pdate)

    # news text
    _text = bsoup.select('#articleBodyContents')[0].get_text().replace('\n', " ")
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(btext.strip())

    # 신문사
    pcompany = bsoup.select('#footer address')[0].a.get_text()
    news_detail.append(pcompany)
    
    #URL
    news_detail.append(n_url)
    return news_detail

#데이터 프레임 생성
columns = ['날짜','신문사', '제목','내용', 'URL']
df = pd.DataFrame(columns=columns)

query = '+코로나 +단계 -백신'
s_date = "2020.11.16"       #2020.8.15 로 끊어서 크롤링
e_date = "2020.11.30"
s_from = s_date.replace(".","") 
e_to = e_date.replace(".","") 
page = 1

#크롤링
while True:
    time.sleep(random.sample(range(3), 1)[0]) #네이버의 감시를 피하기 위해 사용
    print(page) 
    url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=1&field=1&ds=" + s_date + "&de=" + e_date +\
    "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page) 
    
    req = requests.get(url,headers=header) 
    cont = req.content 
    soup = BeautifulSoup(cont, 'html.parser')

    if soup.findAll("a",{"class":"info"}) == [] :
        break 
    for urls in soup.findAll("a",{"class":"info"}): 
        try : 
            if urls.attrs["href"].startswith("https://news.naver.com"): 
                news_detail = get_news(urls.attrs["href"]) 
                df=df.append(pd.DataFrame([[news_detail[1], news_detail[3], news_detail[0], news_detail[2], news_detail[4]]],columns=columns))
                print(news_detail[1])
        except Exception as e:  #오류 표기
            print(e)  
            continue 
    
    page += 10  
#인덱스 초기화
df.reset_index(drop=True, inplace=True)

#댓글====================================================================================
print('==========댓글 크롤링==========')
data = pd.DataFrame()
df_url = [i for i in df['URL']]
for url in df_url :
    #url = url + '&sort=LIKE'
    List=[] 
    oid=url.split("oid=")[1].split("&")[0] 
    aid=url.split("aid=")[1] 
    page=1
    header = { 
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
        # 요청된 페이지의 링크 이전의 웹 페이지 주소
        "referer":url,      #댓글을 크롤링할때 쓰임
    } 
    breq_comm = requests.get(url, headers=header)
    bsoup_comm = BeautifulSoup(breq_comm.content, 'html.parser')
    #이 기사의 날짜
    print(bsoup_comm.select('.t11')[0].get_text()[:11])
    
    while True :         
        c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"+oid+"%2C"+aid+"&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page="+str(page)+"&refresh=false&sort=FAVORITE"  
        c_url
        # 파싱하는 단계입니다.
        r=requests.get(c_url,headers=header) 
        cont=BeautifulSoup(r.content,"html.parser")     
        total_comm=str(cont).split('comment":')[1].split(",")[0]         
        # [^문자들] : 문자들이 아닌 패턴 
        # \ : \뒤에 오는 문자를 글자 그대로 인식하게 함
        # * : 앞 패턴이 0개 이상이어야 함
        #match = 댓글
        match=re.findall('"contents":([^\*]*),"userIdNo"', str(cont))[:10] #댓글 개수 n개 [:n]
        # 댓글을 리스트에 중첩합니다.
        List = list(flatten(List))
        List.append(match)
        #댓글 데이터를 댓글_데이터프레임에 넣기
        df_comment = pd.DataFrame(List)
        data = pd.concat([data, df_comment])#, ignore_index=True)
        break
#인덱스 초기화
data.reset_index(drop = True, inplace = True)

#두 데이터프레임 합치기 (axis = 0이면 밑으로, 1이면 옆으로 붙임.)
df = pd.concat([df, data], axis = 1)

#댓글이 없는 데이터 삭제 (NaN)
df.dropna(inplace = True)

#인덱스 초기화
df.reset_index(drop=True, inplace=True)

#=====================================네이버 맞춤법 교정기====================================#
#댓글에 이모티콘 제거
#!pip install emoji
import emoji 
def remove_emoji(text): 
    return emoji.get_emoji_regexp().sub(u'', text)

from selenium import webdriver
from imp import reload
from selenium.webdriver.common.keys import Keys

reload(sys)


user_dir = r'C:\Users\gwqt1\Desktop\chromedriver.exe'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(user_dir, chrome_options=options)

driver.get("https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=2&acq=%EB%A7%9E%EC%B6%A4&qdt=0&ie=utf8&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0")
time.sleep(3)

for I in range(len(df)):
    for i in range(10):
        df[i][I] = remove_emoji(df[i][I])
        
        #클릭 한번 하기.
        driver.find_element_by_xpath("""//*[@id="grammar_checker"]/div/div[2]/div[1]/div[1]/div/div[1]/textarea""").click()
        time.sleep(.1)
        
        #맞춤법 검사기에 값 입력
        driver.find_element_by_xpath("""//*[@id="grammar_checker"]/div/div[2]/div[1]/div[1]/div/div[1]/textarea""").send_keys(df[i][I])
        time.sleep(.1)
        
        #검사 클릭
        driver.find_element_by_xpath("""//*[@id="grammar_checker"]/div/div[2]/div[1]/div[1]/div/div[2]/button""").click()
        time.sleep(1)

        #결과값 저장
        df[i][I] = driver.find_element_by_xpath("""//*[@id="grammar_checker"]/div/div[2]/div[1]/div[2]/div/div[1]/p""").text
        time.sleep(.1)
        
        #X 누르기
        driver.find_element_by_xpath("""//*[@id="grammar_checker"]/div/div[2]/div[1]/div[1]/div/div[2]/span/span/button""").click()
        time.sleep(.1)
        print('Index :', I, 'colmns :',i)

#종료
driver.quit()

#저장
#df.to_json(r'C:\Users\gwqt1\Desktop\df1.json')
#df.to_json(r'C:\Users\gwqt1\Desktop\df2.json')
#데이터 불러오기
df1 = pd.read_json(r'C:\Users\gwqt1\Desktop\df1.json', encoding = 'cp949')
df2 = pd.read_json(r'C:\Users\gwqt1\Desktop\df2.json', encoding = 'cp949')
#병합
df = pd.concat([df2, df1], axis = 0)
df.reset_index(drop=True, inplace=True)
#최종본 저장
df.to_json(r'C:\Users\gwqt1\Desktop\df.json')
