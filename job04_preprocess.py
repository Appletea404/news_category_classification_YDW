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
# okt = Okt()
# okt_x = okt.morphs(X[0])
# print(okt_x)
# okt_x_stem = okt.morphs(X[0], stem=True)
# print(okt_x_stem)

# komoran = Komoran()
# komoran_x = komoran.morphs(X[0])
# print(komoran_x)

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
with open('./data/encoder.pkl', 'wb') as f:
    pickle.dump(label, f)   # pickle: 형변환하지않고 그대로 저장 , f(file)에 label을 붙여 dump에 저장
onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])

# 한글빼고 다 버리기
# cleaned_x = re.sub('[^가-힣]', ' ', X[0])
# print(X[0])
# print(cleaned_x)
okt = Okt()
X = list(X)
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i], stem=True)
    if i % 1000 == 0:
        print(i)
print(X[:5])
for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)
print(X[:5])

# tokenizer(각 형태소에 번호를 붙이는 방법)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
tokened_x = tokenizer.texts_to_sequences(X)
print(tokened_x)
wordsize = len(tokenizer.word_index) + 1
print(wordsize)
max = 0
for sentence in tokened_x:
    if max < len(sentence):
        max = len(sentence)
print(max)
with open('./data/tokenizer_max{}.pkl'.format(max), 'wb') as f:
    pickle.dump(tokenizer, f)

x_pad = pad_sequences(tokened_x, maxlen=max)
print(x_pad[:5])

x_train, x_test, y_train, y_test = train_test_split(
    x_pad, onehot_y, test_size=0.1)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
np.save('./data/x_train_wordsize{}.npy'.format(wordsize), x_train)
np.save('./data/y_train_wordsize{}.npy'.format(wordsize), y_train)
np.save('./data/x_test_wordsize{}.npy'.format(wordsize), x_test)
np.save('./data/y_test_wordsize{}.npy'.format(wordsize), y_test)














