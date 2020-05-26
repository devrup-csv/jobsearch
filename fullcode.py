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

#starting with the main module for scrapping naukri. time.sleep has been used judiciously to prevent abuse of host server.

while x!=0:
    soup=BeautifulSoup(driver.page_source,'html.parser')
    soup1=soup.find_all("article",{"class":"jobTuple bgWhite br4 mb-8"})
    for item in soup1:
        time.sleep(5)
        d={}
        desc=item.find("div",{"class":"job-description fs12 grey-text"}).text
        try:
            clock=re.sub("[a-zA-Z\D]","",item.find("div",{"class":"type br2 fleft grey"}).text)
        except:
            clock=0
        if len(desc)>=70 and int(clock)<=17:
            time.sleep(5)
            d["id"]=item.get("data-job-id")
            d["link_post"]=item.find("a",{"class":"title fw500 ellipsis"}).get("href")
            driver.execute_script("window.open('about:blank', 'tab3');")
            driver.switch_to.window("tab3")
            driver.get(str(d["link_post"]))
            soup=BeautifulSoup(driver.page_source,'html.parser')
            try:
                j=soup.find("div",{"class":"jd-header-comp-name"}).text
                d["company_name"]=re.sub("[0-9]","",re.sub("[\(\[].*?[\)\]]","",j))
            except:
                j=item.find("div",{"class":"mt-7 companyInfo subheading lh16"}).text
                d["company_name"]=re.sub("[0-9]","",re.sub("[\(\[].*?[\)\]]","",j))
            d["name_hash"]=str(d["company_name"]).replace(" ","")
            try:
                d["experience"]=soup.find("div",{"class":"exp"}).text
            except:
                d["experience"]=item.find("li",{"class":"fleft grey-text br2 placeHolderLi experience"}).text
            try:
                d["experience_lower"]=soup.find("div",{"class":"exp"}).text.split()[0]
                d["experience_upper"]=soup.find("div",{"class":"exp"}).text.split()[2]
            except:
                try:
                    d["experience_lower"]=re.sub("[-]"," ",item.find("li",{"class":"fleft grey-text br2 placeHolderLi experience"}).text.split()[0]).split()[0]
                    d["experience_upper"]=re.sub("[-]"," ",item.find("li",{"class":"fleft grey-text br2 placeHolderLi experience"}).text.split()[0]).split()[4]
                except:
                    pass
            try:
                d["salary_lower"]=re.sub("[,]","",soup.find("div",{"class":"salary"}).text.split()[1])
                d["salary_upper"]=re.sub("[,]","",soup.find("div",{"class":"salary"}).text.split()[4])
            except:
                try:
                    d["salary_lower"]=re.sub("[,]","",item.find("li",{"class":"fleft grey-text br2 placeHolderLi salary"}).text.split()[1])
                    d["salary_upper"]=re.sub("[,]","",item.find("li",{"class":"fleft grey-text br2 placeHolderLi salary"}).text.split()[4])
                except:
                    pass
            try:
                d["salary_lcs"]=int(int(d["salary_lower"])/100000)
            except:
                pass
            if d["company_name"] not in gem_list and d["company_name"] not in normal_list:
                try:
                    if int(d["experience_lower"])<=6 and int(d["salary_lower"])>=500000:
                        
                        try:
                            r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor jobss")
                            soup5=BeautifulSoup(r.text,'html.parser')
                            rating=float(re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1])))
                            people=int(re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2])))
                        except:
                            try:
                                r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor")
                                soup5=BeautifulSoup(r.text,'html.parser')
                                rating=float(re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1])))
                                people=int(re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2])))
                            except:
                                driver.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor jobss")
                                soup5=BeautifulSoup(driver.page_source,'html.parser')
                                soup6=soup5.find_all("div",{"class":"g"})[1].find("div",{"class","dhIWPd f"}).text
                                rating=float(re.sub("[A-Za-z\u200e]","",soup6).split()[1])
                                people=int(re.sub("[A-Za-z\u200e,]","",soup6).split()[3])

                        if rating>3.8 and people>10 or rating>3 and people>=140:
                            d["glassdoor_ratings"]=str(rating)
                            d["people_rated"]=str(people)
                            print("gem found")
                            gem+=1
                except:
                    pass
                try:
                    if gem!=1:
                        try:
                            r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor jobss")
                            soup5=BeautifulSoup(r.text,'html.parser')
                            rating=float(re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1])))
                            people=int(re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2])))
                            normal_list.append(d["company_name"])
                        except:
                            try:
                                r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor")
                                soup5=BeautifulSoup(r.text,'html.parser')
                                rating=float(re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1])))
                                people=int(re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2])))
                                normal_list.append(d["company_name"])
                            except:
                                driver.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor jobss")
                                soup5=BeautifulSoup(driver.page_source,'html.parser')
                                soup6=soup5.find_all("div",{"class":"g"})[1].find("div",{"class","dhIWPd f"}).text
                                rating=float(re.sub("[A-Za-z\u200e]","",soup6).split()[1])
                                people=int(re.sub("[A-Za-z\u200e,]","",soup6).split()[3])
                                normal_list.append(d["company_name"])
                        if rating>3.5 and people>1500:
                            d["glassdoor_ratings"]=str(rating)
                            d["people_rated"]=str(people)
                            print("gem found")
                            gem+=1
                except:
                    pass
            else:
                not_unique+=1
                    
            try:
                details=soup.find_all("div",{"class":"details"})
                for each in details:
                    try:
                        d[str(each.find("label").text)]=str(each.find("a").text)
                    except:
                        d[str(each.find("label").text)]=str(each.find("span").text)
            except:
                details=soup.find_all("p",{"class":"coPE"})
                for each in details:
                    try:
                        d[str(each.find("em").text)]=str(each.find_all("span")[1].text)
                    except:
                        pass
            try:
                details2=soup.find("div",{"class":"key-skill"})
                details3=details2.find_all("a")
                i=1
                for each2 in details3:
                    d["skill_tag "+str(i)]=str(each2.text)
                    i+=1
                    if i>8:
                        break
            except:
                try:
                    details2=item.find("ul",{"class":"tags has-description"})
                    details3=details2.find_all("li")
                    i=1
                    for each2 in details3:
                        d["skill_tag "+str(i)]=str(each2.text)
                        i+=1
                        if i>8:
                            break
                except:
                    pass

            try:
                d["jd"]=soup.find("div",{"class":"dang-inner-html"}).text
            except:
                try:
                    d["jd"]=item.find("div",{"class":"job-description fs12 grey-text"}).text
                except:
                    pass
            no_job=0
            l.append(d)
            try:
                d["role_hash1"]=str(d["skill_tag 1"]).replace(" ","")
                d["role_hash2"]=str(d["skill_tag 2"]).replace(" ","")
                d["role_hash3"]=str(d["skill_tag 3"]).replace(" ","")
                role_hash=1
            except:
                pass
            if gem>=1 and str(d["company_name"]) not in company_post:
                gem_list.append(d["company_name"])
                try:
                    d["linkedin_post"]="#hiringalert #covid19 #bschools #freshposts #glassdoorjobss #recruitment2020"+"\n"+str(d["company_name"])+" is hiring for "+str(d["Role"])+" with a minimum experience of "+str(d["experience"])+". Minimum salary offered is "+str(d["salary_lcs"])+"lpa. This company is rated "+str(d["glassdoor_ratings"])+" at glassdoor by "+str(d["people_rated"])+" people. Click on the given link to apply::\n"+str(d["link_post"])+"\nPlease share this post as much as possible, and like or comment so that a needy person may be able to see it.  #helpinghand #jobseeker #automation #jobs #"+str(d["role_hash1"])+" #"+str(d["role_hash2"])+" #hiring #jobvengers #analytics #"+str(d["name_hash"])
                except:
                    d["linkedin_post"]="#hiringalert\nHola fellow Jobvengers. "+str(d["company_name"])+" is recruiting and are looking for skills in "+str(d["skill_tag 1"])+" "+str(d["skill_tag 2"])+" with a minimum experience of "+str(d["experience"])+". This company is rated "+str(d["glassdoor_ratings"])+" at Glassdoor by "+str(d["people_rated"])+" people. Click on the given link to apply\n "+str(d["link_post"])+"\nPlease SHARE this post as much as possible, and LIKE or COMMENT so that a needy person may be able to see it. \n #freshjobs #covid19 #analytics #bschools #freshposts #glassdoorjobss #recruitment2020 #hireme #lookingforjobchange #lookingforajob #jobhunting #helpinghand #jobseeker #automation #jobs #hiring #jobvengers #"+str(d["name_hash"])
                g.append(d)
                driver.switch_to.window(driver.window_handles[1])
                try:
                    driver.find_element(By.XPATH,"//button[contains(@class,'share-box__open share-box__trigger p4 hoverable-link-text t-16 t-black--light t-bold')]").click()
                    time.sleep(1)
                except:
                    element = driver.find_element_by_xpath("//button[contains(@class,'share-box__open share-box__trigger p4 hoverable-link-text t-16 t-black--light t-bold')]")
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.execute_script("window.scrollBy(0,-260);")
                    time.sleep(2)
                    driver.find_element(By.XPATH,"//button[contains(@class,'share-box__open share-box__trigger p4 hoverable-link-text t-16 t-black--light t-bold')]").click()
                try:
                    driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                except:
                    try:
                        element = driver.find_element_by_xpath("//div[@class='ql-editor ql-blank']//p")
                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        driver.execute_script("window.scrollBy(0,-260);")
                        time.sleep(2)
                        driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                    except:
                        try:
                            element = driver.find_element_by_xpath("//div[@class='ql-editor ql-blank']//p")
                            #driver.execute_script("arguments[0].scrollIntoView();", element)
                            driver.execute_script("window.scrollBy(0,-260);")
                            time.sleep(4)
                            driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                        except:
                            time.sleep(3)
                            driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                            
                            

                # driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                with open("gem_list2.txt", "wb") as fp:
                    pickle.dump(gem_list, fp)
                with open("normal_list2.txt", "wb") as fp:
                    pickle.dump(normal_list, fp)
                try:
                    time.sleep(2)
                    driver.find_element(By.XPATH,"//span[text()='Post']").click()
                except:
                    element = driver.find_element_by_xpath("//span[text()='Post']")
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.execute_script("window.scrollBy(0,-240);")
                    time.sleep(1)
                    driver.find_element(By.XPATH,"//span[text()='Post']").click()
                driver.switch_to.window(driver.window_handles[0])
                company_post.append(d["company_name"])
                time.sleep(1)
                gem=0
            else:
                if not_unique==1:
                    g.append(d)
                    not_unique=0
                gem=0
                  
        else:
            no_job+=1

    if no_job>15:
        break   
    x+=1  
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    try:
        driver.find_element(By.XPATH,"//div[@class='fleft pages']//a[contains(text(),'"+str(x)+"')]").click()
    except:
        print("done")
        break
    time.sleep(3)
    print(x)
# pd.DataFrame(l).to_csv("alljobs2.csv")
# pd.DataFrame(g).to_csv("bestjobs2.csv")

#indeed jobs posting module
driver.get("https://www.indeed.co.in/jobs?q=marketing&l=India&sort=date&start=510&vjk=1f62593b9ec54523")
driver.find_element(By.XPATH,"//a[contains(text(),'date')]").click()
time.sleep(2)
driver.execute_script("window.open('about:blank', 'tab2');")
driver.switch_to.window("tab2")
driver.get("https://www.linkedin.com/company/42849051")
input("please login linkedin")
driver.switch_to.window(driver.window_handles[0])
x=1
company_post=[]
not_unique=0
l=[] 
gem=0
with open("gem_list.txt", "rb") as fp:
    gem_list=pickle.load(fp)
with open("normal_list.txt", "rb") as fp:
    normal_list=pickle.load(fp)
g=[]
no_job=1
while x!=0:
    soup=BeautifulSoup(driver.page_source,"html.parser")
    soup1=soup.find_all("div",{"class":"jobsearch-SerpJobCard unifiedRow row result clickcard"})
    box=0
    for item in soup1:
        d={}
        desc=re.sub("[\n]","",item.find("div",{"class":"summary"}).text)
        try:
            clock=re.sub("[a-zA-Z\D+]","",item.find("span",{"class":"date "}).text)
        except:
            clock=0
        if len(desc)>=20 and int(clock)<=17:
            d["id"]=item.get("id")
            try:
                try:
                    driver.find_element(By.XPATH,"//a[@id='sja"+str(box)+"']").click()
                except:
                    try:
                        f=item.find("a",{"class":"jobtitle turnstileLink"}).get("id")
                        driver.find_element(By.XPATH,"//a[@id='"+str(f)+"']").click()
                    except:
                        f=item.find("a",{"class":"jobtitle turnstileLink visited"}).get("id")
                        driver.find_element(By.XPATH,"//a[@id='"+str(f)+"']").click()
            except:
                pass
            time.sleep(1)
            soup=BeautifulSoup(driver.page_source,'html.parser')
            try:
                d["link_post"]="indeed.co.in"+str(soup.find("a",{"class":"view-apply-button blue-button"}).get("href"))
            except:
                try:
                    d["link_post"]="indeed.co.in"+str(item.find("a",{"class":"jobtitle turnstileLink"}).get("href"))
                except:
                    print("no link")
            try:
                j=item.find("span",{"class":"company"}).text
                d["company_name"]=re.sub("[0-9\n-]","",re.sub("[\(\[].*?[\)\]]","",j))
            except:
                j=soup.find("span",{"class":"vjs-cn"}).text
                d["company_name"]=re.sub("[0-9\n-]","",re.sub("[\(\[].*?[\)\]]","",j))
            d["name_hash"]=str(d["company_name"]).replace(" ","")
            soup2=soup.find_all("div",{"class":"jobMetadataHeader-itemWithIcon icl-u-textColor--secondary"})
            try:
                exp=str(soup2[1].find("span",{"class":"jobMetadataHeader-itemWithIcon-icon jobMetadataHeader-itemWithIcon-icon-resume"}))
                if len(exp)>10:
                    d["experience"]=soup2[1].text
                    d["experience_lower"]=re.sub("[+]","",soup2[1].text.split()[0])
                    d["experience_upper"]=">"+str(d["experience_lower"])
                else:
                    exp=str(soup2[1].find("span",{"class":"jobMetadataHeader-itemWithIcon-icon jobMetadataHeader-itemWithIcon-icon-salary"}))
                    if len(exp)>10:
                        d["salary_lower"]=re.sub("[a-zA-Z\D]","",soup2[1].text.split()[0])
                        d["salary_upper"]=re.sub("[a-zA-Z\D]","",soup2[1].text.split()[2])
                        
            except:
                pass
            try:
                
            
                exp=str(soup2[2].find("span",{"class":"jobMetadataHeader-itemWithIcon-icon jobMetadataHeader-itemWithIcon-icon-resume"}))
                if len(exp)>10:
                    d["experience"]=soup2[2].text
                    d["experience_lower"]=re.sub("[+]","",soup2[2].text.split()[0])
                    d["experience_upper"]=">"+str(d["experience_lower"])
                else:
                    exp=str(soup2[2].find("span",{"class":"jobMetadataHeader-itemWithIcon-icon jobMetadataHeader-itemWithIcon-icon-salary"}))
                    if len(exp)>10:
                            
                        d["salary_lower"]=re.sub("[a-zA-Z\D]","",soup2[2].text.split()[0])
                        d["salary_upper"]=re.sub("[a-zA-Z\D]","",soup2[2].text.split()[2])
                        
            except:
#                 try:
#                     d["salary_lower"]=re.sub("[,]","",item.find("li",{"class":"fleft grey-text br2 placeHolderLi salary"}).text.split()[1])
#                     d["salary_upper"]=re.sub("[,]","",item.find("li",{"class":"fleft grey-text br2 placeHolderLi salary"}).text.split()[4])
#                 except:
                pass
            
            if d["company_name"] not in gem_list and d["company_name"] not in normal_list:
                try:
                    if int(d["salary_lower"])>=500000:
                        d["salary_lcs"]=int(int(d["salary_lower"])/100000)
                        try:
                            r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor jobss")
                            soup5=BeautifulSoup(r.text,'html.parser')
                            rating=re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1]))
                            people=re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2]))
                        except:
                            r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor")
                            soup5=BeautifulSoup(r.text,'html.parser')
                            rating=re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1]))
                            people=re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2]))
                        if float(rating)>3 and int(people)>200:
                            d["glassdoor_ratings"]=str(rating)
                            d["people_rated"]=str(people)
                            print("gem found")
                            gem+=1
                except:
                    pass
                try:
                    if gem!=1:
                        try:
                            r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor jobss")
                            soup5=BeautifulSoup(r.text,'html.parser')
                            rating=re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1]))
                            people=re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2]))
                            normal_list.append(d["company_name"])
                        except:
                            r=requests.get("https://www.google.com/search?q="+str(d["company_name"])+" glassdoor")
                            soup5=BeautifulSoup(r.text,'html.parser')
                            rating=re.sub("[()]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[1]))
                            people=re.sub("[(),]","",str(soup5.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text.split()[2]))
                            normal_list.append(d["company_name"])                     
                        if float(rating)>3.5 and int(people)>3000:
                            d["glassdoor_ratings"]=str(rating)
                            d["people_rated"]=str(people)
                            print("gem found")
                            gem+=1
                except:
                    pass
            else:
                not_unique+=1
                
            d["role"]=re.sub("[\n.]","",item.find("h2",{"class":"title"}).text)
            d["role_hash"]=str(d["role"]).replace(" ","")
            try:
                d["jd"]=re.sub("[\n]","",soup.find("div",{"id":"vjs-desc"}).text)
                
            except:
                try:
                    d["jd"]=re.sub("[\n]","",item.find("div",{"class":"summary"}).text)
                except:
                    pass
            
            l.append(d)
            no_job=0
            #linkedin posting module
            if gem>=1:
                gem_list.append(d["company_name"])
                try:
                    d["linkedin_post"]="#hiringalert #operationsjobs #covid19 #bschools #freshposts #glassdoorjobss #recruitment2020"+"\n"+str(d["company_name"])+" is hiring for "+str(d["role"])+" with a minimum experience of "+str(d["experience"])+".Minimum salary offered is "+str(d["salary_lcs"])+"lpa.This company is rated "+str(d["glassdoor_ratings"])+" at glassdoor by "+str(d["people_rated"])+"\n people.Click on the given link to apply "+str(d["link_post"])+" Please share this post as much as possible, and like or comment so that a needy person may be able to see it.  #helpinghand #jobseeker #automation #jobs #hiring #jobvengers #analytics #"+str(d["name_hash"])+" #"+str(d["role_hash"])
                except:
                    d["linkedin_post"]="#hiringalert #operationsjobs\nHola fellow Jobvengers. "+str(d["company_name"])+" is recruiting for "+str(d["role"])+". This company is rated "+str(d["glassdoor_ratings"])+" at Glassdoor by "+str(d["people_rated"])+" people. Click on the given link to apply\n "+str(d["link_post"])+"\nPlease SHARE this post as much as possible, and LIKE or COMMENT so that a needy person may be able to see it. \n #freshjobs #covid19 #analytics #bschools #freshposts #glassdoorjobss #recruitment2020 #hireme #lookingforjobchange #lookingforajob #jobhunting #helpinghand #jobseeker #automation #jobs #hiring #jobvengers #"+str(d["name_hash"])+" #"+str(d["role_hash"])
                g.append(d)
                driver.switch_to.window(driver.window_handles[1])
                try:
                    driver.find_element(By.XPATH,"//button[contains(@class,'share-box__open share-box__trigger p4 hoverable-link-text t-16 t-black--light t-bold')]").click()
                    time.sleep(1)
                except:
                    element = driver.find_element_by_xpath("//button[contains(@class,'share-box__open share-box__trigger p4 hoverable-link-text t-16 t-black--light t-bold')]")
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.execute_script("window.scrollBy(0,-260);")
                    time.sleep(2)
                    driver.find_element(By.XPATH,"//button[contains(@class,'share-box__open share-box__trigger p4 hoverable-link-text t-16 t-black--light t-bold')]").click()
                try:
                    driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                except:
                    try:
                        element = driver.find_element_by_xpath("//div[@class='ql-editor ql-blank']//p")
                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        driver.execute_script("window.scrollBy(0,-260);")
                        time.sleep(2)
                        driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                    except:
                        element = driver.find_element_by_xpath("//div[@class='ql-editor ql-blank']//p")
                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        driver.execute_script("window.scrollBy(0,-260);")
                        time.sleep(4)
                        driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))

                # driver.find_element(By.XPATH,"//div[@class='ql-editor ql-blank']//p").send_keys(str(d["linkedin_post"]))
                with open("gem_list.txt", "wb") as fp:
                    pickle.dump(gem_list, fp)
                with open("normal_list.txt", "wb") as fp:
                    pickle.dump(normal_list, fp)
                try:
                    time.sleep(2)
                    driver.find_element(By.XPATH,"//span[text()='Post']").click()
                except:
                    element = driver.find_element_by_xpath("//span[text()='Post']")
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.execute_script("window.scrollBy(0,-240);")
                    time.sleep(1)
                    driver.find_element(By.XPATH,"//span[text()='Post']").click()
                driver.switch_to.window(driver.window_handles[0])
                company_post.append(d["company_name"])
                time.sleep(1)
                gem=0
            else:
                if not_unique==1:
                    g.append(d)
                    not_unique=0
                  
        else:
            no_job+=1
        box+=1

    if no_job>15:
        break   
    x+=1  
    time.sleep(1)
    try:
        print("trying")
        
        driver.find_element(By.XPATH,"//span[@class='pn'][contains(text(),'"+str(x)+"')]").click()
    except:
        print("done")
        break
    time.sleep(3)
    
   #aggregating of al excel sheets should be done before wordcloud formation
  #wordcloud module for jd
df=pd.read_csv("/GD/My Drive/calci/jobsmay.csv")
X=df.jd
mask = np.array(Image.open(r'/GD/My Drive/calci/jobs2.jpg'))
# plt.imshow(mask)
# plt.axis("off")
stop_words = ["i", "me","business","customer","program","employee","using","position","candidate","jobs","understanding","identify","related","organization","new","understand","delivery","report","market","design","platform","develop","manage","organiation","tech""understanding","partner","need","activity","plan","good","role","working","based","work","drive","within","various","ability","ensure","application","including","year","required","development","industry","product","knowledge","provide","process","company","service","requirement","solution","etc","project","client","my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the","Mr", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
def remove_stopwords(text):
    word_list = text.split()
    word_list = [word for word in word_list if word not in stop_words]
    text = ' '.join(word_list)
    return text
corpus=[]
for i in range(0,len(X)):
    jobs=re.sub(r'\W',' ',str(X[i]))
    jobs=jobs.lower()
    jobs=re.sub(r'\s+[a-z]\s+',' ',jobs)
    jobs=re.sub(r'^[a-z]\s+',' ',jobs)
    jobs=re.sub(r'\s+',' ',jobs)
    jobs=re.sub(r"^http://t.co/[a-zA-Z0-9]*\s"," ",jobs)
    jobs=re.sub(r"\s+http://t.co/[a-zA-Z0-9]*\s"," ",jobs)
    jobs=re.sub(r"\s+http://t.co/[a-zA-Z0-9]*$"," ",jobs)
    jobs=re.sub(r"\d"," ",jobs)
    lemmer=WordNetLemmatizer()
    ww=nltk.word_tokenize(jobs)
    ww=[word for word in ww if word not in stopwords.words('english')]
    newwords=[lemmer.lemmatize(word) for word in ww]
    #     newwords=[stemmer.stem(word) for word in ww]
    jobs=' '.join(newwords)
    jobs=remove_stopwords(jobs)
    corpus.append(jobs)
text=""
for item in corpus:
  text=text+item    
wordcloud = WordCloud(mask=mask, width=2000, height=1000,contour_color="black", max_words=10000,relative_scaling = 0, background_color = "white").generate(text)
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[20,15])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
_=plt.show()
