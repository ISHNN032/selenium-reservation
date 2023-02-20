#-*- coding:utf-8 -*-
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
URL = "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S221014174755769728#"

PATH12 = "/html/body/div/div[3]/div[2]/div/form[2]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[7]/a/span[2]/div/span"
PATH19 = "/html/body/div/div[3]/div[2]/div/form[2]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[7]/a/span[2]/div/span"

# 크롤링 옵션 생성
options = webdriver.ChromeOptions()
# 백그라운드 실행 옵션 추가
options.add_argument("headless")
driver = webdriver.Chrome(r'chromedriver', chrome_options= options)

driver.get(url=URL)

isFull = True
while(isFull):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, PATH12))
        )
        count12 = driver.find_element(By.XPATH, PATH12).text
        count19 = driver.find_element(By.XPATH, PATH19).text
        print("12:" + count12 + " 19:" + count19)
        isFull = count12 == "25/25" and count19 == "25/25"
    except TimeoutException:
        print('Time Out')
    finally:
        if(isFull == True):
            randsleep = random.uniform(1.1, 10.0)
            print("\t\t\tretry in .." + str(randsleep))
            time.sleep(randsleep)
            driver.refresh()
print("the reservation is valied!")