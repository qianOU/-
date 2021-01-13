# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

from normalize_text import normalized_corpus, tokenize_text

texts = [
    'the sky is beautiful',
    'i like this sky',
    'the clound is white and bird is singing',
    'we want to go hiking'
    ]

test = ['happy day the sky is cheerful']

def display(array, columns):
    df = pd.DataFrame(array, columns=columns)
    print(df)
    return df 

df = CountVectorizer(min_df=1, ngram_range=(1,1)).fit(texts)
feature_names = df.get_feature_names()
print(feature_names)
display(df.transform(texts).todense(), feature_names)
display(df.transform(test).todense(), feature_names)

# In[TF-IDF]
#TfidfVectorizer 可直接作用在文本数据上
#TfidfTransformer 不可以直接作用在文本数据上，需要基于词袋模型的输出
from sklearn.feature_extraction.text import TfidfVectorizer

df = TfidfVectorizer(min_df=1, ngram_range=(1,1), norm='l2').fit(texts)
feature_names = df.get_feature_names()
print(feature_names)
display(np.round(df.transform(texts).todense(), 2), feature_names)
display(np.round(df.transform(test).todense(), 2), feature_names)
df.vocabulary_ #得到tfidf的词汇表和列数之间的映射关系                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
# In[word2vec 高级词向量]
import gensim
import nltk

tonkenized_texts = [nltk.word_tokenize(sentence) for sentence in texts]
tonkenized_test = [nltk.word_tokenize(sentence) for sentence in test]

#build word2vec model
model = gensim.models.Word2Vec(tonkenized_texts, size=10, window=5, 
                               sample=1e-3, min_count=2)
model.wv['sky']

#获取词汇
words = model.wv.index2word
print(words)

## 获取对应词向量
vectors = model.wv.vectors
print(vectors)  

#获取相似性

print(model.wv.similarity('the', 'sky'))

#上述是为每一个单词创建一个词向量表示
#将词向量进行汇总为文档向量
#其一平均词向量AVW

def average_word_vectors(words, model, vocabulary, num_features):
    feature_vector = np.zeros((num_features, ), dtype=np.float)
    matched = 0
    
    for word in words:
        if word in vocabulary:
            matched += 1
            feature_vector = feature_vector + model.wv[word]
        if matched:
            feature_vector = feature_vector / matched
    
    return feature_vector

#prepare above function for a corpus of documents
def average_word_vectorizer(tokenize_sentences, model, num_features):
    vocabulary = model.wv.index2word
    features = [average_word_vectors(words, model, vocabulary, num_features)
                for words in tokenize_sentences]
    return np.array(features)

example = """
I am a newbie to the net, and I am trying to get some information for a paper\nI am working on to get back into college.  If anyone can send me data on\nSolar coronal holes and recurrant aurora  for the past thirty years it would be\na big help.  Or, if you have information on more esoteric things like Telluric\ncurrent, surge bafflers power companies use, or other effects sporatic aurora\nhave on the Earth's magnetic field, I'd be eternally gratefull.  Please send \nanything interesting to me at\n        Marty Crandall-Grela\n        Van Vleck Observatory\n        Wesleyan University\n        Middletown,Ct 06487\n or e-mail it to me at mcrandall@eagle.wesleyan.edu\n Thank-you in advance,      Marty\n\n
"""
#每一个子列表代表一个document
tokens = normalized_corpus([example, example], tokenize=True) #需要确认使用高级词向量是否需要去除停用词等

model = gensim.models.Word2Vec(tokens, size=30, window=6, min_count=1)

average_word_vectorizer(tokens, model, 30)


## TF-IDF 加权平均词向量

def tfidf_avg_word_vector(words, tfidf_vector, tfidf_vocabulary, model, num_features):
    word_tfidf = [tfidf_vector[0, tfidf_vocabulary.get(word)] if tfidf_vocabulary.get(word)
                   else 0 for word in words]
    word_tfidf_map = {word: tfidf_val for word, tfidf_val in zip(words, word_tfidf)}
    
    feature_vector = np.zeros((num_features, ), dtype=np.float)
    vocabulary = set(model.wv.index2word)
    wts = 0
    for word in words:
        if word in vocabulary:
            word_vector = model.wv[word]
            weighted_word_vector = word_vector*word_tfidf_map[word]
            wts += word_tfidf_map[word]
            feature_vector = feature_vector + weighted_word_vector
    if wts:
        feature_vector = feature_vector / wts
    
    return feature_vector

def tfidf_weighted_avg_word_vectorizer(corpus, tfidf_vector,
                                       tfidf_vocabulary, model, num_features):
    
    doc_tfidfs = [(doc, doc_tfidf) for doc, doc_tfidf in zip(corpus, tfidf_vector)]
    features = [tfidf_avg_word_vector(words, tfidf, tfidf_vocabulary, model, num_features)
                for words, tfidf  in doc_tfidfs]
    return np.array(features)

# example
tokenized_texts = [tokenize_text(i) for i in texts]
from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer(ngram_range=(1,1)).fit(texts)
tfidf_vectors = tf.transform(texts).todense()
vocabulary = tf.vocabulary_
model = gensim.models.Word2Vec(tokenized_texts, size=30, window=6, min_count=1)
tfidf_weighted_avg_word_vectorizer(tokenized_texts, tfidf_vectors, vocabulary, model, 30)
     