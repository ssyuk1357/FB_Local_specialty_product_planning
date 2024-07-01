# 셀레니움으로 카카오 네비 들어가기
# 사용 불가 => 카카오 네비 확률적 변경
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#By를 통해 경로를 어떤걸 쓸지 사용.
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from tqdm import tqdm
import time
from selenium.webdriver.common.by import By

# 크롬 옵션 설정
# 크롬 웹드라이버 설치 및 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window() # 브라우저 전체화면
# get 메
li = []
url = 'https://cafe.naver.com/cjyeonsu'
driver.get(url)
time.sleep(20)
driver.find_element(By.XPATH, '//*[@id="menuLink372"]').click()
time.sleep(3)

# iframe으로 전환
driver.switch_to.frame("cafe_main")
# driver.find_element(By.XPATH, '//*[@id="main-area"]/div[6]/a[3]').click()
# time.sleep(3)
# driver.find_element(By.XPATH, '//*[@id="main-area"]/div[4]/table/tbody/tr[1]/td[1]/div[2]/div/a[1]').click()
# time.sleep(3)
# html = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div')
# print(html.text)

# # 게시판 진입
# board = driver.find_element(By.CSS_SELECTOR, f"#menuLink{board_dict[city]}")
# driver.implicitly_wait(3)
# board.click()
#
# # iframe으로 전환
# driver.switch_to.frame("cafe_main")
#
# 게시판별 첫 번째 게시글 클릭
driver.find_element(By.XPATH, '//*[@id="main-area"]/div[4]/table/tbody/tr[1]/td[1]/div[2]/div/a[1]').click()
time.sleep(1)
data_text = []
data_title = []
num_conts = 500
for i in tqdm(range(1, num_conts)):
    try:
        cont_url = driver.find_element(By.XPATH, '//*[@id="spiButton"]').get_attribute('data-url')
        cont_num = cont_url.split("/")[-1]
        cont_date = driver.find_element(By.CLASS_NAME, 'date').text
        cont_author = driver.find_element(By.CLASS_NAME, 'nickname').text
        cont_title = driver.find_element(By.CLASS_NAME, 'title_text').text
        cont_text = driver.find_element(By.CLASS_NAME, 'se-main-container').text
    except:
        pass

    # 게시물 작성 날짜가 2021년 이전일 경우 탐색 중지, 다음 게시판으로 이동
    if cont_date[:4] <= '2020':
        break

    # 2020년 이후의 데이터는 data 딕셔너리에 추가
    else:
        data_text.append(cont_text)
        data_title.append(cont_title)

    # 다음 게시물로 이동
    try:
        driver.find_element(By.CSS_SELECTOR,
                            "#app > div > div > div.ArticleTopBtns > div.right_area > a.BaseButton.btn_next.BaseButton--skinGray.size_default").click()
    except:
        driver.find_element(By.CSS_SELECTOR,
                            "#app > div > div > div.ArticleTopBtns > div.right_area > a.BaseButton.btn_next.BaseButton--skinGray.size_default > span").click()
    time.sleep(3)

    # 게시물을 1000개 탐색할 때마다 JSON 파일로 데이터 백업
df_cafe = pd.DataFrame()
df_cafe['cafe_text'] = data_text
df_cafe['cafe_title'] = data_title
df_cafe.to_csv('네이버_카페.csv', encoding = 'utf-8-sig')