# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:25:26 2021

@author: 28659
"""
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