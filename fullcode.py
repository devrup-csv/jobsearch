from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import msvcrt
import requests
import pickle
import json
import time

driverlocation="C:\\monday2\\chromedriver.exe"
os.environ["webdriver.chrome.driver"]=driverlocation #during final compilation, packaging of chrome driver also required
driver=webdriver.Chrome(driverlocation) #mandatory for getting webdriver 
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(driverlocation,options=options)
driver.get("https://www.naukri.com/mba-jobs?k=mba&ctcFilter=101&ctcFilter=6to10&ctcFilter=10to15&ctcFilter=15to25&ctcFilter=50to75&ctcFilter=75to100&ctcFilter=25to50&jobAge=15&experience=5")
driver.find_element(By.XPATH,"//i[@class='naukicon naukicon-arrow-1']").click()
driver.find_element(By.XPATH,"//li[contains(text(),'Date')]").click()
time.sleep(2)
driver.execute_script("window.open('about:blank', 'tab2');")
driver.switch_to.window("tab2")
driver.get("https://www.linkedin.com/company/42849051")
input("please login linkedin")
driver.switch_to.window(driver.window_handles[0])
gem_list=[]
x=1
role_hash=0
l=[] 
gem=0
not_unique=0
g=[]
no_job=1
normal_list=[]
# with open("gem_list2.txt", "rb") as fp:
#     gem_list=pickle.load(fp)
# with open("normal_list2.txt", "rb") as fp:
#     normal_list=pickle.load(fp)
