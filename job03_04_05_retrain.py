import pickle
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from konlpy.tag import Okt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, MaxPooling1D, LSTM, Dropout, Flatten, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# ===== job03: 데이터 합치기 =====
df1 = pd.read_csv('./data/news_titles.csv')
df2 = pd.read_csv('./data/naver_news_today_20260608_1101.csv')
df = pd.concat([df1, df2], ignore_index=True)
df = df.drop_duplicates()
print(df.category.value_counts())
df.to_csv('./data/news_titles_retrain.csv', index=False)

# ===== job04: 전처리 =====
X = list(df.titles)
Y = df.category

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
label = encoder.classes_
with open('./data/encoder.pkl', 'wb') as f:
    pickle.dump(label, f)
onehot_y = to_categorical(labeled_y)

okt = Okt()
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i], stem=True)
    if i % 1000 == 0:
        print(i)

for idx, sentence in enumerate(X):
    words = [word for word in sentence if len(word) > 1]
    X[idx] = ' '.join(words)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
tokened_x = tokenizer.texts_to_sequences(X)
wordsize = len(tokenizer.word_index) + 1
max_len = max(len(s) for s in tokened_x)
print('wordsize:', wordsize, 'max_len:', max_len)

with open('./data/tokenizer_max{}.pkl'.format(max_len), 'wb') as f:
    pickle.dump(tokenizer, f)

x_pad = pad_sequences(tokened_x, maxlen=max_len)
x_train, x_test, y_train, y_test = train_test_split(x_pad, onehot_y, test_size=0.1)
np.save('./data/x_train_wordsize{}.npy'.format(wordsize), x_train)
np.save('./data/y_train_wordsize{}.npy'.format(wordsize), y_train)
np.save('./data/x_test_wordsize{}.npy'.format(wordsize), x_test)
np.save('./data/y_test_wordsize{}.npy'.format(wordsize), y_test)

# ===== job05: 모델 학습 =====
model = Sequential()
model.add(Embedding(wordsize, 300))
model.build(input_shape=(None, max_len))
model.add(Conv1D(32, 5, padding='same', activation='relu'))
model.add(MaxPooling1D(1))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(32, activation='tanh'))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(6, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(x_train, y_train, batch_size=128, epochs=10, validation_data=(x_test, y_test), verbose=1)
score = model.evaluate(x_test, y_test, verbose=0)
print('Final test loss:', score[0])
print('Final test accuracy:', score[1])
model.save('./models/news_section_classfier{}.h5'.format(score[1]))

plt.plot(fit_hist.history['val_accuracy'], label='val accuracy')
plt.plot(fit_hist.history['accuracy'], label='train accuracy')
plt.legend(loc='lower right')
plt.show()
