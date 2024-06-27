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
    x = [i for i in range(1,10)]
    
    #토픽 분석
    for k in range(1,10):
        NUM_TOPICS = k
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
        topics = ldamodel.print_topics(num_words=4)
        
        #coherence, perplexity
        cm = CoherenceModel(model=ldamodel, corpus=corpus, coherence='u_mass')
        coherence = cm.get_coherence()
        coherences.append(coherence)
        perplexities.append(ldamodel.log_perplexity(corpus))
        
        print(k)
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

df_A = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_A.json', encoding = 'cp949')
topic_analy_graph(df_A)

df_B = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_B.json', encoding = 'cp949')
topic_analy_graph(df_B)

df_C = pd.read_json(r'C:\Users\gwqt1\Desktop\텍스트마이닝_레포트\df_전체\df_C.json', encoding = 'cp949')
topic_analy_graph(df_C)

topic_modeling(df_A, 3)

topic_modeling(df_B, 4)

topic_modeling(df_C, 3)

