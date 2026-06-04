# 파일명은 naver_news_section.csv로 해주세요.
# 컬럼명은 titles, category로 해주세요.
# 유동원님이 정치, 경제
# 김수연님이 사회, 문화
# 이석현님이 세계, IT
# 다 되면 PR부탁합니다

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

df_titles = pd.DataFrame()

options = ChromeOptions()
options.add_argument('lang=ko.KR')
options.add_argument('headless')
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# ===== 102 사회 =====
url = 'https://news.naver.com/section/102'
driver.get(url)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]/a'
for i in range(30):
    driver.find_element(By.XPATH, button_xpath).click()
    time.sleep(0.5)
titles = []

for i in range(1, 180):
    for j in range(1, 7):
        try:
            title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
            title = driver.find_element(By.XPATH, title_xpath).text
            print(title)
            titles.append(title)
        except:
            print('error', i, j)

df = pd.DataFrame(titles, columns=['titles'])
df['category'] = 'Social'
df_titles = pd.concat([df_titles, df], ignore_index=True)

# ===== 103 생활/문화 =====
url = 'https://news.naver.com/section/103'
driver.get(url)
time.sleep(1.5)

for i in range(30):
    driver.find_element(By.XPATH, button_xpath).click()
    time.sleep(0.5)
titles = []

for i in range(1, 180):
    for j in range(1, 7):
        try:
            title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
            title = driver.find_element(By.XPATH, title_xpath).text
            print(title)
            titles.append(title)
        except:
            print('error', i, j)

df = pd.DataFrame(titles, columns=['titles'])
df['category'] = 'Culture'
df_titles = pd.concat([df_titles, df], ignore_index=True)

driver.quit()

df_titles.to_csv('./data/naver_news_section_Social_Culture.csv', encoding='utf-8-sig')
print('저장 완료')