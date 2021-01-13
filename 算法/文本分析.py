# In[3.3 词性(pos)标注]

sentences = 'The brown fox is quick anad he is jumping over the lazy dog'

import nltk
tokens = nltk.word_tokenize(sentences)
tagged_sent = nltk.pos_tag(tokens, tagset='universal')
tagged_sent


from pattern.en import tag
tagged_sent = tag(sentences)
print(tagged_sent)

#自己构建词性标注
from nltk.corpus import treebank
data = treebank.tagged_sents()
train_data = data[:3500]
test_data = data[3500:]
print(train_data[0])
#分词
tokens = nltk.word_tokenize(sentences)
tokens

from nltk.tag import DefaultTagger
df = DefaultTagger('NN')
df.tag(tokens)
df.evaluate(test_data)

from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger
ut = UnigramTagger(train_data) #1元
bt = BigramTagger(train_data) # 2~
tr = TrigramTagger(train_data) #3~

ut.evaluate(test_data)
ut.tag(tokens)
bt.evaluate(test_data)
bt.tag(tokens)
tr.evaluate(test_data)
tr.tag(tokens)

#链式功能
def combine_tagger(train_data, taggers, backoff=None):
    for tagger in taggers:
        backoff = tagger(train_data, backoff=backoff)
    return backoff

ct = combine_tagger(train_data, 
                    taggers=[UnigramTagger, BigramTagger, TrigramTagger],
                    backoff=df)

ct.evaluate(test_data)
print(ct.tag(tokens))


# 使用有监督的方法进行词性标注
from nltk.classify import NaiveBayesClassifier, MaxentClassifier
from nltk.tag.sequential import ClassifierBasedPOSTagger

nbt = ClassifierBasedPOSTagger(train=train_data,
                               classifier_builder=NaiveBayesClassifier.train
                               )
nbt.evaluate(test_data)


mcf = ClassifierBasedPOSTagger(train=train_data,
                               classifier_builder=MaxentClassifier.train
                               )
mcf.evaluate(test_data)

# In[3.3.4 浅层分析 shallow parsing]

# In[文本数据规范化]
import nltk

#文本切分
def tokenize_text(text):
    words = nltk.word_tokenize(text)
    word_tokens = [word.strip() for word in words]
    return word_tokens

import re
import string

# 删除特殊字符
def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_token = filter(None, [pattern.sub('', token) for token in tokens])
    return ' '.join(filtered_token)

# 拓展缩写词
# 英语中撇号用于缩写
#isn‘t ---> is not
#导入缩写映射
from contractions import CONTRACTION_MAP
def expand_contractions(sentence, contractions_mapping):
    """
    tricks: 利用正则表达式的sub可以传递函数处理每一个匹配项的功能
    """
    contractions_pattern = re.compile('({})'.format('|'.join(contractions_mapping.keys())
                                                    , flags=re.IGNORECASE|re.DOTALL))
    
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        try:
            expand_contraction = contractions_mapping.get(match) \
                                if contractions_mapping.get(match) \
                                else contractions_mapping.get(match.lower())
            expand_contraction = first_char + expand_contraction[1:]
        except:
            expand_contraction = match
        return expand_contraction
    

    return contractions_pattern.sub(expand_match, sentence)

# for example
expand_contractions("I'm so happy aND i don't like", CONTRACTION_MAP)

# 大小写转换
#upper 与 lower

#删除停用词
def remove_stopwords(text):
    tokens = tokenize_text(text)
    stop_words = nltk.corpus.stopwords.words('english')# 默认会删除·no与not
    stop_words = set(stop_words) - set(['no', 'not']) #保留no与not等单词
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(filtered_tokens)

#矫正拼写错误
def correct_match(match):
    from pattern.en import suggest
    temp = suggest(match)
    print(temp)
    return temp

#example 
correct_match('happpy')

#词干提取 
#词干提取得到的单词不一定是准确的，不一定存在于字典中
from nltk.stem import PorterStemmer, LancasterStemmer
ps = PorterStemmer()
ls = LancasterStemmer()
ps.stem('jummping')
ls.stem('jumpping')

# 词性还原
#去掉后缀，得到存在于字典中的根词
# lemma(词性)
from nltk.stem import WordNetLemmatizer
wl = WordNetLemmatizer()
wl.lemmatize('cars', 'n')
wl.lemmatize('jumping', 'v')
wl.lemmatize('sadest', 'a')

def pos_tag_text(text):
    from pattern.en import tag
    from nltk.corpus import wordnet as wn
    #convert penn treebank tag to wordnet tag
    def penn_to_wn_tags(pos_tag):
        if pos_tag.startswith('J'):
            return wn.ADJ
        if pos_tag.startswith('V'):
            return wn.VERB
        if pos_tag.startswith('N'):
            return wn.NOUN
        if pos_tag.startswith('R'):
            return wn.ADV
        return None
    
    tagged_text = tag(text)
    tagged_lower_text = [(word.lower(), penn_to_wn_tags(pos_tag)) 
                         for word, pos_tag in 
                         tagged_text]
    return tagged_lower_text

#lemmaatize text based on POS tags
#利用pos标签进行词性还原
def lemmatize_text(text):
    from nltk.stem import WordNetLemmatizer as wn
    wnl = WordNetLemmatizer()
    pos_tagged_text = pos_tag_text(text)
    lemmatized_tokens = [wnl.lemmatize(word, pos_tag) if pos_tag else word
                         for word, pos_tag in pos_tagged_text]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text
    lemmatized_tokens = []
    

# 移除数字
def remove_digits(text):
    return re.sub('(\d+)', '', text)
    
    



# 统一api
def normalized_corpus(corpus, tokenize=False):
    """
    Parameters
    ----------
    corpus : list[text]
        DESCRIPTION.
    tokenize : boolean, optional
        DESCRIPTION. The default is False.
    Returns
    -------
    normalized_corpus : TYPE
        DESCRIPTION.

    """

    normalized_corpus = []
    for text in corpus:
        text = expand_contractions(text, CONTRACTION_MAP) #拓展缩写
        text = lemmatize_text(text) # 词性还原
        text = remove_special_characters(text)
        text = remove_stopwords(text)
        text = remove_digits(text)
        if tokenize:
            text = tokenize_text(text)
        normalized_corpus.append(text)
    
    return normalized_corpus

#example
aa = ["i'm happy and going to test!",
      'Honey, go to sleppy?']

normalized_corpus(aa)
 # In[词袋模型]
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np


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
    
# In[实战---新闻分类]
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split


datasets = fetch_20newsgroups(subset='all',
                              shuffle=True,
                              remove=('headers', 'footers', 'quotes'))
X = datasets.data
Y = datasets.target

# 删除空内容
def remove_empty(corpus, labels):
    filtered_corpous = []
    filtered_labels = []
    for i,j in zip(corpus, labels):
        if i.strip():
            filtered_corpous.append(i)
            filtered_labels.append(j)
    
    return filtered_corpous, filtered_labels

X, Y = remove_empty(X, Y)
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.333)

train_x = normalized_corpus(train_x)
test_x = normalized_corpus(test_x)

#转换为tfidf向量
from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer(ngram_range=(1,1), min_df=1,norm='l2').fit(train_x)
train_x = tf.transform(train_x)
test_x = tf.transform(test_x)

#建模
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def evalution(y_true, y_pred):
    print('confusion-matrix', end='\n\r')
    print(confusion_matrix(y_true, y_pred))
    print('accuracy-score:', end='\n\r')
    print(accuracy_score(y_true, y_pred))
    print('precision-score', end='\n\r')
    print(precision_score( y_true, y_pred, average='weighted'))
    print('recall-score', end='\n\r')
    print(recall_score( y_true, y_pred, average='weighted'))
    print('f1-score', end='\n\r')
    print(f1_score( y_true, y_pred, average='weighted'))

model = SVC(kernel='rbf')
model.fit(train_x, train_y)
evalution(train_y, model.predict(train_x))
evalution(test_y, model.predict(test_x))
