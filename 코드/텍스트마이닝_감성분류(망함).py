#감성분류
import re
import pandas as pd

df = pd.read_json(r'C:\Users\gwqt1\Desktop\df_cluster.json', encoding = 'cp949')

#긍정 사전
p = open(r'C:\Users\gwqt1\Desktop\pos_dict.txt', encoding = 'utf-8')
pos_words = []
for line in p.readlines():
    pos_words.append(line.rstrip())
p.close()

#부정 사전
n = open(r'C:\Users\gwqt1\Desktop\neg_dict.txt', encoding = 'utf-8')
neg_words = []
for line in n.readlines():
    neg_words.append(line.rstrip())
n.close()

#
emoti_list = []
for I in range(len(df)):
    pos_score = 0
    neg_score = 0
    for w in df.loc[I]['본문명사토큰']: 
        if w in pos_words: 
            pos_score += 1
        if w in neg_words: 
            neg_score += 1
    if pos_score+neg_score == 0:
        emoti_list.append(0)
    else:
        emoti_list.append(neg_score / (pos_score+neg_score))
        
        
print(emoti_list)
