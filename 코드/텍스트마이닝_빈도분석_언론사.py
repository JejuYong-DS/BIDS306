#빈도분석+시각화
import pandas as pd
#from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#한글 폰트 오류 해결 코드
from matplotlib import font_manager, rc
font_path = r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트_코드\malgun\malgun.ttf'
font_name = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font_name)

def text_analy_graph(df):
    df_list = []
    for I in range(len(df)):    
        df_list += df.loc[I]['본문토큰']
    
    df_count = pd.Series([x for x in df_list if len(x)>1])
    df_count = df_count.value_counts().head(20) #상위 20개

    #막대그래프
    plt.style.use('ggplot')
    df_count.plot(kind = 'bar', figsize = (20,10), width = 0.7, color = 'skyblue')
    plt.xticks(fontsize=24, rotation = 0)
    plt.yticks(fontsize=16, rotation = 0)
    plt.show()

    wc = WordCloud(width = 800, height = 800, font_path = font_path, background_color='white')
    plt.figure(figsize = (10,10))
    plt.imshow(wc.generate_from_frequencies(df_count))

df_A = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트_코드\df_전체\df_A.json', encoding = 'cp949')
text_analy_graph(df_A)

df_B = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트_코드\df_전체\df_B.json', encoding = 'cp949')
text_analy_graph(df_B)

df_C = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트_코드\df_전체\df_C.json', encoding = 'cp949')
text_analy_graph(df_C)


