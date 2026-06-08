import pickle
import pandas as pd
import numpy as np
from keras.utils import to_categorical
from konlpy.tag import Okt
from keras.preprocessing.sequence import pad_sequences
from keras.models import  load_model
import re
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

df = pd.read_csv('./data/naver_headline_news_20260608.csv')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
print(df.category.value_counts())

X = df.title
Y = df.category

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])
X = list(X)
okt = Okt()
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i], stem=True)
print(X)

for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)
print(X[:10])

with open('./data/tokenizer_max26.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
tokened_x = tokenizer.texts_to_sequences(X)
print(tokened_x[:5])

for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 26:
        tokened_x[i] = tokened_x[i][:26]
x_pad = pad_sequences(tokened_x, maxlen=26)
print(x_pad[:5])

model = load_model('./models/news_section_classfier0.694968581199646.h5')
score = model.evaluate(x=x_pad, y=onehot_y, verbose=0)
print('accuracy', score[1])

preds = model.predict(x_pad)
print(preds)
predict_section = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predict_section.append([most,second])
df['predict'] = predict_section
print(df.head(30))

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 1
print(df.OX.mean())















