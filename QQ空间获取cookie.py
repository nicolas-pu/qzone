import re
from selenium import webdriver
import time
import pickle

url="https://qzone.qq.com/"

def getGTK(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff

browser=webdriver.Chrome()
browser.get(url)
time.sleep(10)
print(browser.title)
cookiedict = {}
for cookie in browser.get_cookies():#取cookies
    cookiedict[cookie['name']] = cookie['value']
print('Get the cookie of QQlogin successfully!(共%d个键值对)' % (len(cookiedict)))
html = browser.page_source
g_qzonetoken=re.search(r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)
gtk=getGTK(cookiedict)
browser.quit()
info=(cookiedict,gtk,g_qzonetoken.group(1))
#print(info)
f=open(r"qzoneCookie.txt",'wb')
pickle.dump(info,f)
f.close()
print("Success")
