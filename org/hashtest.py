#-*- coding:utf-8 -*-
import time
import random
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
 
URL = "https://md5.gromweb.com/?md5=6d79e030371e47e6231337805a7a2685"
VALUE_TEXT = "/html/body/div/div[3]/section/article/div[1]/p[1]/em[2]"

# 크롤링 옵션 생성
options = webdriver.ChromeOptions()
# 백그라운드 실행 옵션 추가
options.add_argument("headless")
driver = webdriver.Chrome(r'chromedriver', options= options)

driver.get(url=URL)
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, VALUE_TEXT))
)
wtf = driver.find_element(By.XPATH, VALUE_TEXT).text
print("the reservation is valied!" +  wtf)