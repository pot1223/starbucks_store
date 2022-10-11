!pip install selenium 
!pip install bs4 
!apt-get update # selenium 모듈 최신 업데이트 
!apt install chromium-chromedriver # chromedriver 파일 다운받기
!cp /usr/lib/chromium-browser/chromedriver /usr/bin  # chromedriver 파일 실행가능한 위치로 복사 
!pip install -U requests # 버전 의존관계 error 해결
!pip install pyautogui
!pip install pyperclip


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  #  selenium에서 정보를 찾을 때는 BeautifulSoup를 사용하는 편이 좋다  
import time # 사이트에 접속할때 시간을 주어서 접속해야 오류가 나지 않는다 
import pandas as pd # 엑셀 , csv 파일로 저장할 때 사용  
from selenium.webdriver.common.keys import Keys #자동 스크롤 및 클릭 구현에 사용 


options = webdriver.ChromeOptions()
options.add_argument('--headless') # 브라우저가 보이지 않게 하는 headless 설정 (colab환경에서는 설정해야 한다)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('chromedriver', options=options) # 브라우저 생성


url = "https://www.starbucks.co.kr/store/store_map.do?disp=locale"
browser.get(url)


import time

browser.find_elements(By.CSS_SELECTOR , '.sido_arae_box > li > a')[0].click()
time.sleep(3) 
browser.find_elements(By.CSS_SELECTOR , '.gugun_arae_box> li > a')[0].click()
time.sleep(3) 



html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
starbucks_soup_list = soup.select('li.quickResultLstCon')
starbucks_list = []
for starbucks_store in starbucks_soup_list : 
  name = starbucks_store.select('strong')[0].text.strip()
  lat = starbucks_store['data-lat'].strip() # 위도
  lng = starbucks_store['data-long'].strip() # 경도
  store_type = starbucks_store.select('i')[0]['class'][0][4:]
  address = str(starbucks_store.select('p.result_details')[0]).split('<br/>')[0].split('>')[1]
  tel = str(starbucks_store.select('p.result_details')[0]).split('<br/>')[1].split('<')[0]
  starbucks_list.append([name, lat, lng, store_type, address, tel])
columns = ['매장명', '위도', '경도', '매장타입', ' 주소', '전화번호']
seoul_starbucks_df = pd.DataFrame(starbucks_list, columns = columns)
seoul_starbucks_df.to_csv("seoul_starbucks_df.csv", index = False)
