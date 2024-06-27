import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import nltk
nltk.download('punkt')
import json
import re
from konlpy.tag import Okt


df = pd.read_json(r'C:\Users\gwqt1\Desktop\df_token.json', encoding = 'cp949')
Result_List = []
    
for I in range(len(df)):
    #댓글
    
    token_df_List = []
   
    for i in range(10):
        token_df_List += list([df.loc[I][str(i)]])

    
    text = str(token_df_List)
    
    #본문
    #text = df.loc[I]['내용']
    
    okt=Okt()
    text = okt.nouns(text)
    
    text = [x for x in text if len(x)>=2]
    
    
    p = re.compile("[0-9]+")
    text = p.sub("",str(text))
    p = re.compile("\W+")
    text = p.sub(" ",str(text))
    p =  re.compile("_")
    text = p.sub(" ",str(text))
    p = re.compile("[a-zA-Z]")
    text = p.sub(" ",str(text))
    hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
    text = hangul.sub('', text)
    text = text.split('네이버', 1)[0]
    
    token = word_tokenize(text)    
    stop_file=open(r'C:\Users\gwqt1\Desktop\불용어사전1.txt', encoding='utf-8')
    stop_words=['는','은','이','가','코로나','코로나바이러스','단계','거리','두기','진자']#진자 = 확진자
    for line in stop_file.readlines():
        stop_words.append(line.rstrip())
    stop_file.close()
    
    result = [] 
    for w in token: 
        if w not in stop_words: 
            result.append(w) 
    
    Result_List += list([result])
    
    print(result)
    #시리즈로 만들기
    sr_result = pd.Series(Result_List)
sr_result.name = '댓글토큰' 
df = pd.concat([df,sr_result], axis=1)

df.to_json(r'C:\Users\gwqt1\Desktop\df_token.json')
