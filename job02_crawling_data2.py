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
import datetime

options = ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('headless')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# DataFrame 초기화
df_titles = pd.DataFrame()


url = 'https://news.naver.com/section/101'
# 카테고리 마다 URL 설정

# //*[@id="newsct"]/div[5]/div/div[2]/a

driver.get(url)
button_xpath = '//*[@id="newsct"]/div[5]/div/div[2]/a'
for i in range(30):
    driver.find_element(By.XPATH, button_xpath).click()
    time.sleep(0.5)




for i in range(1,180):
    for j in range(1,7):
        try:
            # //*[@id="newsct"]/div[5]/div/div[1]/div[2]/ul/li[2]/div/div/div[2]/a/strong
            title_xpath = '//*[@id="newsct"]/div[5]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i,j)
            title = driver.find_element(By.XPATH, title_xpath).text
            print(title)
            df_section_titles = pd.DataFrame([title], columns=['titles'])
            df_section_titles['category'] = 'Economic'
            df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
        except:
            print('error',i,j)

df_titles.to_csv('./data/naver_news_section_Economic.csv', index=False)


