#군집분류
import pandas as pd

#날짜별 단계 ==========================================================
df = pd.read_json(r'C:\Users\gwqt1\Desktop\df_token.json', encoding = 'cp949')
df['날짜'] = df['날짜'].str.replace('.', '').astype(int)

step_list = []
for I in range(len(df)):
    if df.loc[I]['날짜'] <= 20200222:
        step_list.append(0)
    elif df.loc[I]['날짜'] <= 20200505 and df.loc[I]['날짜'] >= 20200223:
        step_list.append(3)
    elif df.loc[I]['날짜'] <= 20200815 and df.loc[I]['날짜'] >= 20200506:
        step_list.append(1)
    elif df.loc[I]['날짜'] <= 20200829 and df.loc[I]['날짜'] >= 20200816:
        step_list.append(2)
    elif df.loc[I]['날짜'] <= 20200913 and df.loc[I]['날짜'] >= 20200830:
        step_list.append(2.5)
    elif df.loc[I]['날짜'] <= 20201011 and df.loc[I]['날짜'] >= 20200914:
        step_list.append(2)
    elif df.loc[I]['날짜'] <= 20201107 and df.loc[I]['날짜'] >= 20201012:
        step_list.append(1)
    elif df.loc[I]['날짜'] <= 20201119 and df.loc[I]['날짜'] >= 20201108:
        step_list.append(1.5)
    elif df.loc[I]['날짜'] <= 20201127 and df.loc[I]['날짜'] >= 20201120:
        step_list.append(2)
    elif df.loc[I]['날짜'] <= 20201129 and df.loc[I]['날짜'] >= 20201128:
        step_list.append(2)
    else :
        step_list.append(3)
    
sr_step = pd.Series(step_list)
sr_step.name = '단계'
df = pd.concat([df,sr_step], axis=1)

#언론사 =================================================================
A_list = ['조선일보', '중앙일보', '동아일보', 'donga.com', '문화일보', '국민일보', '뉴데일리', '독립신문', '데일리안', '한국논단', '천지일보', '뉴스라이브', '아시아투데이', 'cnb뉴스', '브레이크뉴스', '데일리NK', '쿠키뉴스', '연합뉴스', 'YTN', '한국경제', '매일경제', '서울경제', '헤럴드경제', '아시아경제', '이투데이', '동아사이언스', '매경닷컴', '매일신문','한국경제TV', '한경닷컴','아시아경제신문' '디지털타임스', '헬스조선', 'Joins.com', '조선비즈', '뉴스1', '연합뉴스TV', '머니S', '아시아경제신문', '디지털타임스']
B_list = ['서울신문', '한국일보', '내일신문', '뉴시스', '파이낸셜뉴스', 'financial news', 'eTimesinternet Co', 'SBS CNBC', '더팩트', '채널A', 'media KHAN', '강원일보', '부산일보', 'KBS', 'MBN', 'SBS & SBSi ', '디지털데일리', 'MBC', '일간스포츠', 'inews24.com', 'ZDNet Korea', '조세일보', '세계닷컴']
C_list = ['한겨레 신문', '프레시안', '오마이뉴스', '경향신문', '딴지일보', '시사in', '미디어오늘', '노컷뉴스(CBS)', '머니투데이', '이데일리', '레디앙', '미디어스', '민중의 소리', '머니투데이', '이데일리',  'PRESSian', 'MoneyToday', 'The Internet Hankyoreh', '노컷뉴스', 'OhmyNews', 'edaily', '여성신문', '시사저널', 'JTBC']
Press_list = []
for I in range(len(df)):
    if df.loc[I]['신문사'] in A_list:
        Press_list.append(1)
    elif df.loc[I]['신문사'] in B_list:
        Press_list.append(2)
    elif df.loc[I]['신문사'] in C_list:
        Press_list.append(3)
    else:
        print('문제 있음')
        
sr_press = pd.Series(Press_list)
sr_press.name = '신문사성향(1:보수,2:중립,3:진보)'
df = pd.concat([df,sr_press], axis=1)

df.to_json(r'C:\Users\gwqt1\Desktop\df_cluster.json')
