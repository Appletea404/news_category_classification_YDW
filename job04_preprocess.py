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