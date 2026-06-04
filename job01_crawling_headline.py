from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime


category = ['Politics', 'Economic', 'Social', 'Culture', 'World','IT']
df_titles = pd.DataFrame()

url = 'https://news.naver.com/section/100'
resp = requests.get(url)
# print(list(resp))

soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup)

title_tag = soup.select('.sa_text_strong')
# print(title_tag)
print(title_tag[0].text)
