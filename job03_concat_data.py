import pandas as pd

df = pd.read_csv('./data/naver_news_section_World.csv')
print(df.head())

df_temp = pd.read_csv('./data/naver_news_section_IT.csv')
print(df_temp.head())

df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_news_section_Economic.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_news_section_Politics.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_news_section_Social_Culture_clean.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('./data/naver_headline_news_20260605.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df.info()
df = df.drop_duplicates()
print(df.category.value_counts())
print(df.isnull().sum())
df.info()
df.to_csv('./data/news_titles.csv', index=False)