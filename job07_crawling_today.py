from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime

options = ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('headless')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# (URL, 카테고리명, div 인덱스) - 경제(101)만 div[5], 나머지 div[4]
sections = [
    ('https://news.naver.com/section/100', 'Politics', 4),
    ('https://news.naver.com/section/101', 'Economic', 5),
    ('https://news.naver.com/section/102', 'Social',   4),
    ('https://news.naver.com/section/103', 'Culture',  4),
    ('https://news.naver.com/section/104', 'World',    4),
    ('https://news.naver.com/section/105', 'IT',       4),
]

df_all = pd.DataFrame()

for url, category, div_num in sections:
    driver.get(url)
    time.sleep(1.5)

    button_xpath = '//*[@id="newsct"]/div[{}]/div/div[2]/a'.format(div_num)
    for i in range(30):
        try:
            driver.find_element(By.XPATH, button_xpath).click()
            time.sleep(0.5)
        except:
            print('{} 더보기 {}회 오류'.format(category, i))
            break

    titles = []
    for i in range(1, 180):
        for j in range(1, 7):
            try:
                title_xpath = '//*[@id="newsct"]/div[{}]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(div_num, i, j)
                title = driver.find_element(By.XPATH, title_xpath).text
                titles.append(title)
            except:
                pass

    df = pd.DataFrame(titles, columns=['titles'])
    df['category'] = category
    df_all = pd.concat([df_all, df], ignore_index=True)
    print('{}: {}개 수집'.format(category, len(titles)))

driver.quit()

df_all = df_all.drop_duplicates()
print(df_all.category.value_counts())

filename = './data/naver_news_today_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M'))
df_all.to_csv(filename, index=False)
print('저장 완료: {}'.format(filename))
