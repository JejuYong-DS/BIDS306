#토픽분석
import pandas as pd
import matplotlib.pyplot as plt
from gensim import corpora
import gensim
import pyLDAvis.gensim
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.coherencemodel import CoherenceModel

def topic_analy_graph(df):
    df_list = []
    for I in range(len(df)):    
        df_list.append(df.loc[I]['본문토큰'])
    
    dictionary = corpora.Dictionary(df_list)
    corpus = [dictionary.doc2bow(text) for text in df_list]
    print(corpus[I]) #(token, count)

    coherences=[]
    perplexities=[]
    x = [i for i in range(1,20)]
    
    #토픽 분석
    for k in range(1,20):
        NUM_TOPICS = k
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
        topics = ldamodel.print_topics(num_words=4)
        
        #coherence, perplexity
        cm = CoherenceModel(model=ldamodel, corpus=corpus, coherence='u_mass')
        coherence = cm.get_coherence()
        coherences.append(coherence)
        perplexities.append(ldamodel.log_perplexity(corpus))
        
    #시각화 - coherence, perplexity
    plt.plot(x,coherences)
    plt.ylabel('coherences')
    plt.show()
    
    plt.plot(x,perplexities) 
    plt.ylabel('perplexities')
    plt.show()
    
    #시각화 - LDAvis
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
    pyLDAvis.display(vis)
    pyLDAvis.save_html(vis, r'C:\Users\gwqt1\Desktop\vis.html') #하나씩 저장하고 이름 바꿔야함

#토픽 모델링    
def topic_modeling(df, k):
    vectorizer = CountVectorizer(min_df=0)
    
    tfidf = TfidfTransformer()
    np.set_printoptions(precision=2)    
    
    revised_reviews = []
    for I in range(len(df)):
        revised_reviews += [i for i in df.loc[I]['본문토큰']]
    vector_reviews = vectorizer.fit_transform(revised_reviews)
    vectorizer.get_feature_names()
    
    model=LatentDirichletAllocation(n_components=k)#k 수정
    model.fit(vector_reviews)
    
    for topic_index, topic in enumerate(model.components_):
            
        print('Topic #',topic_index+1)
        topic_index = topic.argsort()[::-1] 
        
        feature_names = ' '.join([vectorizer.get_feature_names()[i] for i in topic_index[:5]])
        print(feature_names)

df_0 = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_0.json', encoding = 'cp949')
topic_analy_graph(df_0)

df_1 = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_1.json', encoding = 'cp949')
topic_analy_graph(df_1)

df_1_5 = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_1_5.json', encoding = 'cp949')
topic_analy_graph(df_1_5)

df_2 = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_2.json', encoding = 'cp949')
topic_analy_graph(df_2)

df_2_5 = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_2_5.json', encoding = 'cp949')
topic_analy_graph(df_2_5)

df_3 = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_3.json', encoding = 'cp949')
topic_analy_graph(df_3)


topic_modeling(df_0, 4)
topic_modeling(df_1, 8)
topic_modeling(df_1_5, 6)
topic_modeling(df_2, 6)
topic_modeling(df_2_5, 3)
topic_modeling(df_3, 5)




