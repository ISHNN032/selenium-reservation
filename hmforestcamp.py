#-*- coding:utf-8 -*-
import sys
import time
import random
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_SUBMIT_BUTTON = "/html/body/div[5]/div/div/article/form/p/button"
ELECTRIC_CHECKBOX_NAME = "b20190906a14ae7d914132"

uid = sys.argv[1]
pw = sys.argv[2]

if len(sys.argv) == 5: #[filename, id, pass, deck, date]
    spec_deck = 65 - int(sys.argv[3])
    spec_date = sys.argv[4]
    PATH = f"https://hmforestcamp.com/Reservation/?idx={spec_deck}&day={spec_date}"
    
else:
    spec_deck = 65 - int(sys.argv[3])
    PATH = "http://hmforestcamp.com/Reservation"

# 크롤링 옵션 생성
options = webdriver.ChromeOptions()
# 백그라운드 실행 옵션 추가
options.add_argument("headless")
driver = webdriver.Chrome(r'chromedriver', chrome_options= options)

driver.get(url=PATH)

def login():
    try:
        logged_in = driver.find_element(By.CLASS_NAME, "use_info")
    except NoSuchElementException:
        print("not logged in")
        logged_in = None
    if(logged_in == None):
        user_icon = driver.find_element(By.CLASS_NAME, "icon-user")
        driver.execute_script("arguments[0].click();", user_icon)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, LOGIN_SUBMIT_BUTTON))
        )
        username = driver.find_element(By.NAME, "uid")
        password = driver.find_element(By.NAME, "passwd")
        username.send_keys(uid)
        password.send_keys(pw)
        login_btn = driver.find_element(By.XPATH, LOGIN_SUBMIT_BUTTON)
        login_btn.submit()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "use_info"))
        )
        print("login succeed")

def purchase():
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, ELECTRIC_CHECKBOX_NAME))
    )
    electric_check = driver.find_element(By.NAME, ELECTRIC_CHECKBOX_NAME)
    driver.execute_script("arguments[0].click();", electric_check)
    driver.execute_script("SITE_BOOKING.addBooking(false);")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "cash_idx"))
    )
    cash_select = driver.find_element(By.ID, "cash_idx")
    sss = driver.execute_script("return arguments[0].selected=true;", cash_select)

    cancel_check = driver.find_element(By.NAME, "agree_cancel")
    driver.execute_script("arguments[0].click();", cancel_check)
    purchase_check = driver.find_element(By.ID, "paymentAllCheck")
    driver.execute_script("arguments[0].click();", purchase_check)

    pay_btn = driver.find_element(By.CLASS_NAME, "_btn_start_payment")
    pay_btn.submit()
    return True

login()

needRefresh = False
done = False
while(not done):
    try:
        if needRefresh:
            driver.refresh()
        if purchase():
            done = True
            print("the reservation is valied!")
    except TimeoutException:
        print('Time Out')
    except UnexpectedAlertPresentException:
        print('UnexpectedAlertPresentException')
        needRefresh = True
        time.sleep(5)
    finally:
        print('Loops')
print('END')