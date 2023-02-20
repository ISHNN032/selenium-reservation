#-*- coding:utf-8 -*-
import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

itemPage = "https://yeyak.seoul.go.kr/web/search/selectPageListDetailSearchImg.do?code=T500&dCode=T502"

jspageSrc = "fnDetailPage(**id**);"
itemName = "/html/body/div[1]/div[3]/div[2]/div/div[3]/ul/li[1]/a/div[2]/h4"
itemName2 = "/html/body/div[1]/div[3]/div[2]/div/div[3]/ul/li[6]/a/div[2]/h4"

nameScribt = "document.querySelector(\"#contents > div:nth-child(10) > ul > li:nth-child(6) > a\").onclick.toString().match(/\'S[0-9]*/g).toString().substring(1)"

paths = {
    'a': "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S230211144124694015",
    'b': "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S230211145025248959",
    'c': "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S230211150020900809",
    'd': "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S230211150852224390"
}
sample = "/html/body/div/div[3]/div[2]/div/form[2]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[7]/a/span[2]/div/span"

# 크롤링 옵션 생성
options = webdriver.ChromeOptions()
# 백그라운드 실행 옵션 추가
options.add_argument("headless")
driver = webdriver.Chrome(r'chromedriver', chrome_options= options)

driver.get(url=paths[sys.argv[1]])

needRefresh = False
isFull = True
while(isFull):
    try:
        if needRefresh:
            driver.refresh()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, sample))
        )
        title = driver.execute_script("return Yjs.Gnb.jqObj.news[0].children[1].innerText;")
        print(title)
        result = "result: "
        for i in range(3, 5):
            path = "/html/body/div/div[3]/div[2]/div/form[2]/div[1]/div[1]/div[2]/div/table/tbody/tr[%d]/td[7]/a/span[2]/div/span"%i
            count = driver.find_element(By.XPATH, path).text
            result += " " + count
            if(count != "24/24" and count != "19/19" and count != "13/13" and count != "26/26"):
                isFull = False
        print(result)

        needRefresh = True
    except TimeoutException:
        print('Time Out')
    finally:
        if(isFull == True):
            randsleep = random.uniform(1.1, 5.0)
            print("\tretry in .." + str(randsleep))
            time.sleep(randsleep)
            driver.refresh()
print("the reservation is avaliable!")