'''
selenium login to qzone, get cookie and other useful information
'''
import re
from selenium import webdriver
import time
import pickle

def getGTK(cookiedict):
    hashes = 5381
    if 'p_skey' in cookiedict:
        for letter in cookiedict['p_skey']:
            hashes += (hashes << 5) + ord(letter)
        return hashes & 0x7fffffff
    else:
        return

def getInfo(url):
    browser=webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    #print(browser.title)
    cookiedict = {}
    for cookie in browser.get_cookies():
        cookiedict[cookie['name']] = cookie['value']
    #print('Get the cookie of QQlogin successfully!(共%d个键值对)' % (len(cookiedict)))
    html = browser.page_source
    browser.quit()
    g_qzonetoken=re.search(r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)
    gtk=getGTK(cookiedict)
    if gtk and g_qzonetoken:
        info=(cookiedict,gtk,g_qzonetoken.group(1))
    else:
        info=None
    #print(info)
    return info

def writeToTxt(txtUrl,info):
    if info:
        f=open(txtUrl,'wb')
        pickle.dump(info,f)
        f.close()
        print("get cookie successfully")
    else:
        print("get cookie wrong")

def getQzoneCookie(txtUrl):
    url="https://qzone.qq.com/"
    info=getInfo(url)
    writeToTxt(txtUrl,info)
    return info

if __name__=="__main__":
    txtUrl='qzoneInfo.txt'
    print(getQzoneCookie(txtUrl))
    
