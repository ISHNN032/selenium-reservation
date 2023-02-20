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
 
URL = "http://hmforestcamp.com/Reservation?idx=55&day=2023-01-14"
# URL = "http://hmforestcamp.com/Reservation/?idx=53&day=2022-10-27"
PATH_LOGIN_SUBMIT_BUTTON = "/html/body/div[5]/div/div/article/form/p/button"
PATH_PROFILE_ICON = "/html/body/header/div/div/div[2]/div/div[3]/div/div[3]/div[2]/div/div/div/div/div[2]/div/a[2]/img"

# 크롤링 옵션 생성
options = webdriver.ChromeOptions()
# 백그라운드 실행 옵션 추가
options.add_argument("headless")
driver = webdriver.Chrome(r'chromedriver', chrome_options= options)

driver.get(url=URL)

needRefresh = False
isFull = True
while(isFull):
    try:
        if needRefresh:
            driver.get(driver.current_url)
            # driver.refresh()
            # driver.execute_script("location.reload()")
        try:
            logged_in = driver.find_element(By.CLASS_NAME, "use_info ")
        except NoSuchElementException:
            logged_in = None

        if(logged_in == None):
            driver.execute_script("SITE_MEMBER.openLogin('L1Jlc2VydmF0aW9uP2lkeD01NSZkYXk9MjAyMy0wMS0xNA%3D%3D', 'null', null, 'N');")
            # driver.execute_script("SITE_MEMBER.openLogin('L1Jlc2VydmF0aW9uLz9pZHg9NTMmZGF5PTIwMjItMTAtMjc%3D', 'null', null, 'Y');")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, PATH_LOGIN_SUBMIT_BUTTON))
            )
            username = driver.find_element(By.NAME, "uid")
            password = driver.find_element(By.NAME, "passwd")
            username.send_keys("ishnn032n@gmail.com")
            password.send_keys("m6098m@!")
            login_btn = driver.find_element(By.XPATH, PATH_LOGIN_SUBMIT_BUTTON)
            login_btn.submit()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, PATH_PROFILE_ICON))
        )
        electric_check = driver.find_element(By.NAME, "b20190906a14ae7d914132")
        driver.execute_script("arguments[0].click();", electric_check)

        driver.execute_script("SITE_BOOKING.addBooking(false);")


        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "order_detail"))
        )
        driver.execute_script("let cash = PAY_CASH_TEMPLATE; cash.ariaSelected = 0;")

        cancel_check = driver.find_element(By.NAME, "agree_cancel")
        driver.execute_script("arguments[0].click();", cancel_check)
        purchase_check = driver.find_element(By.ID, "paymentAllCheck")
        driver.execute_script("arguments[0].click();", purchase_check)

        pay_btn = driver.find_element(By.CLASS_NAME, "_btn_start_payment")
        driver.execute_script("arguments[0].click();", pay_btn)
        
        isFull = False
        print('Done')
    except TimeoutException:
        print('Time Out')
    except UnexpectedAlertPresentException:
        print('UnexpectedAlertPresentException')
        alert = Alert(driver)
        print(alert.text)
        alert.accept()
        needRefresh = True
        time.sleep(5)
    finally:
        print('Loops\n')


print("the reservation is valied!")