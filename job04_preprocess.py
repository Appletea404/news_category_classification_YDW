import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt, Komoran
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import re

df = pd.read_csv('./data/news_titles.csv')
df.info()
print(df.head(30))
print(df.category.value_counts())

X = df.titles
Y = df.category
# print(X[0])
# # 데이터를 형태소 분리를 시킴
# okt = Okt()
# okt_x = okt.morphs(X[0])
# print(okt_x)
#
# komoran = Komoran()
# komoran_x = komoran.morphs(X[0])
# print(komoran_x)

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
with open('./data/encoder.pkl', 'wb') as f:
    pickle.dump(label, f)
onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])

# 특수문자/숫자 제거 (한글, 영문, 공백만 남김)
for i in range(len(X)):
    X[i] = re.sub('[^가-힣a-zA-Z ]', ' ', X[i])

# 형태소 분리 (stem=True 로 어간 추출)
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
    if i % 1000 == 0:
        print(i)
print(X[:5])

# 한 글자 단어 및 불용어 제거
try:
    stopwords = list(pd.read_csv('./data/stopwords.csv', index_col=0)['stopword'])
except FileNotFoundError:
    stopwords = []
for sentence in range(len(X)):
    words = []
    for word in X[sentence]:
        if len(word) > 1 and word not in stopwords:
            words.append(word)
    X[sentence] = ' '.join(words)
print(X[:5])

# 토큰화 (단어 -> 정수 인덱스)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
tokened_x = tokenizer.texts_to_sequences(X)
wordsize = len(tokenizer.word_index) + 1
print('wordsize:', wordsize)
with open('./data/news_token.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

# 가장 긴 문장 길이에 맞춰 패딩
max_len = 0
for i in range(len(tokened_x)):
    if max_len < len(tokened_x[i]):
        max_len = len(tokened_x[i])
print('max_len:', max_len)
x_pad = pad_sequences(tokened_x, max_len)
print(x_pad[:5])

# 학습/검증 데이터 분리
x_train, x_test, y_train, y_test = train_test_split(
    x_pad, onehot_y, test_size=0.1)
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

np.save('./data/x_train_wordsize{}'.format(wordsize), x_train)
np.save('./data/x_test_wordsize{}'.format(wordsize), x_test)
np.save('./data/y_train_wordsize{}'.format(wordsize), y_train)
np.save('./data/y_test_wordsize{}'.format(wordsize), y_test)