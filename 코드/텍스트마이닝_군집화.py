#군집화
import pandas as pd

df = pd.read_json(r'C:\Users\gwqt1\Desktop\df_cluster.json', encoding = 'cp949')

#colu = ['날짜','신문사','제목','내용','URL','0','1','2','3','4','5','6','7','8','9','본문토큰', '댓글토큰','단계','신문사성향(1:보수,2:중립,3:진보)']
df_0 = pd.DataFrame()
df_1 = pd.DataFrame()
df_1_5 = pd.DataFrame()
df_2 = pd.DataFrame()
df_2_5 = pd.DataFrame()
df_3 = pd.DataFrame()

for I in range(len(df)):
    if df.loc[I]['단계'] == 0:
        sr_cluster = df.iloc[I]
        df_0 = pd.concat([df_0, sr_cluster], axis=1)
        
    if df.loc[I]['단계'] == 1:
        sr_cluster = df.iloc[I]
        df_1 = pd.concat([df_1, sr_cluster], axis=1)
        
    if df.loc[I]['단계'] == 1.5:
        sr_cluster = df.iloc[I]
        df_1_5 = pd.concat([df_1_5, sr_cluster], axis=1)
        
    if df.loc[I]['단계'] == 2:
        sr_cluster = df.iloc[I]
        df_2 = pd.concat([df_2, sr_cluster], axis=1)
        
    if df.loc[I]['단계'] == 2.5:
        sr_cluster = df.iloc[I]
        df_2_5 = pd.concat([df_2_5, sr_cluster], axis=1)
        
    if df.loc[I]['단계'] == 3:
        sr_cluster = df.iloc[I]
        df_3 = pd.concat([df_3, sr_cluster], axis=1)


df_0 = df_0.T
df_1 = df_1.T
df_1_5 = df_1_5.T
df_2 = df_2.T
df_2_5 = df_2_5.T
df_3 = df_3.T

df_0 = df_0.reset_index(drop = True)
df_1 = df_1.reset_index(drop = True)
df_1_5 = df_1_5.reset_index(drop = True)
df_2 = df_2.reset_index(drop = True)
df_2_5 = df_2_5.reset_index(drop = True)
df_3 = df_3.reset_index(drop = True)

df_0.to_json(r'C:\Users\gwqt1\Desktop\df_0.json')
df_1.to_json(r'C:\Users\gwqt1\Desktop\df_1.json')
df_1_5.to_json(r'C:\Users\gwqt1\Desktop\df_1_5.json')
df_2.to_json(r'C:\Users\gwqt1\Desktop\df_2.json')
df_2_5.to_json(r'C:\Users\gwqt1\Desktop\df_2_5.json')
df_3.to_json(r'C:\Users\gwqt1\Desktop\df_3.json')

#=========================================#

df_A = pd.DataFrame()
df_B = pd.DataFrame()
df_C = pd.DataFrame()

for I in range(len(df)):
    if df.loc[I]['신문사성향(1:보수,2:중립,3:진보)'] == 1:
        sr_cluster = df.iloc[I]
        df_A = pd.concat([df_A, sr_cluster], axis=1)
        
    if df.loc[I]['신문사성향(1:보수,2:중립,3:진보)'] == 2:
        sr_cluster = df.iloc[I]
        df_B = pd.concat([df_B, sr_cluster], axis=1)
        
    if df.loc[I]['신문사성향(1:보수,2:중립,3:진보)'] == 3:
        sr_cluster = df.iloc[I]
        df_C = pd.concat([df_C, sr_cluster], axis=1)

#A : 보수, B : 중립, C:진보
df_A = df_A.T
df_B = df_B.T
df_C = df_C.T

df_A = df_A.reset_index(drop = True)
df_B = df_B.reset_index(drop = True)
df_C = df_C.reset_index(drop = True)

df_A.to_json(r'C:\Users\gwqt1\Desktop\df_A.json')
df_B.to_json(r'C:\Users\gwqt1\Desktop\df_B.json')
df_C.to_json(r'C:\Users\gwqt1\Desktop\df_C.json')
