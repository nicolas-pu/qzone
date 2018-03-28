'''
selenium login to qzone, get cookie and other useful information
if cookie was get successfully, friendlist will be got soon
config.py load QQnumber and password
'''

import re
import time
import json
from selenium import webdriver
import requests
from config import QQNumber,QQPassword
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
}
INFO= None
FriendList={}


def get_login_info(qqNumber=QQNumber, qqPassword=QQPassword):
    browser = webdriver.Chrome()
    browser.get("https://qzone.qq.com/")
    time.sleep(1)
    browser.switch_to_frame("login_frame")
    browser.find_element_by_id("switcher_plogin").click()
    browser.find_element_by_id("u").send_keys(qqNumber)
    browser.find_element_by_id("p").send_keys(qqPassword)
    browser.find_element_by_id("login_button").click()
    time.sleep(1)
    if browser.title == "QQ空间-分享生活，留住感动":
        print("错误")
        return
    print("成功登陆")
    infoDict = {}
    for cookie in browser.get_cookies():
        infoDict[cookie['name']] = cookie['value']
    html = browser.page_source
    browser.quit()
    g_qzonetoken = re.search(r'window\.g_qzonetoken = \(function\(\)\{ try\{return \"(.*?)\";\} catch\(e\)', html)
    gtk = get_GTK(infoDict)
    if gtk and g_qzonetoken:
        global INFO
        INFO = (QQNumber, infoDict, gtk, g_qzonetoken.group(1))
    else:
        pass
    return


def get_GTK(infoDict):
    hashes = 5381
    if 'p_skey' in infoDict:
        for letter in infoDict['p_skey']:
            hashes += (hashes << 5) + ord(letter)
        return hashes & 0x7fffffff
    else:
        return


def login_and_get_friendList():
    qqNumber, cookies, gtk, g_qzonetoken=INFO
    params = {
        'hat_seed': '1',
        'uin': qqNumber,
        'fupdate': '1',
        'g_tk': str(gtk),
        'qzonetoken': g_qzonetoken}
    try:
        s = requests.session()
        response = s.request('GET',
                             'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_hat_get.cgi',
                             params=params, headers=headers, cookies=cookies)
    except requests.exceptions.ConnectionError:
        print("Connected to network failed"
              "FriendList get failed")
        return
    global FriendList
    if response:
        data = response.text.replace("_Callback(", '').replace(");", '')
        friend = json.loads(data).get("data")
        if friend is not None:
            for i in friend:
                if i != "activity":
                    FriendList[i] = friend[i]['realname']


get_login_info()
login_and_get_friendList()







# def write_to_txt(infoName, info):
#     f = open(infoName, 'wb')
#     pickle.dump(info, f)
#     f.close()
#     print("get new info successfully")


# def testInfo(info):
#     s = requests.session()
#     if not info:
#         return False
#     qqnumber, cookies, gtk, g_qzonetoken = info
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
#         'Accept': '*/*',
#         'Accept-Language': 'zh-CN,zh;q=0.8',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive'
#     }
#     params = {
#         'uin': qqnumber,
#         'ftype': '0',
#         'sort': '0',
#         'pos': '0',
#         'num': '20',
#         'replynum': '100',
#         'callback': '_preloadCallback',
#         'code_version': '1',
#         'format': 'jsonp',
#         'need_private_comment': '1',
#         'g_tk': str(gtk),
#         'qzonetoken': g_qzonetoken
#     }
#     try:
#         response = s.request('GET',
#                              'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
#                              params=params, headers=headers, cookies=cookies)
#     except requests.exceptions.ConnectionError:
#         print("Connected to network failed")
#     if response and response.status_code == 200:
#         text = response.text.replace("_preloadCallback(", '').replace(");", '').replace("_Callback(", '')
#         data = json.loads(text)
#         if data["message"] == "请先登录空间":
#             return False
#         else:
#             return True
#
# def getInfo(infoUrl="qzoneInfo.txt"):
#     if os.path.exists(infoUrl):
#         try:
#             with open(infoUrl, 'rb') as f:
#                 info = pickle.load(f)
#         except pickle.UnpicklingError:
#             info = None
#         else:
#             info = get_login_info()
#     else:
#         info = get_login_info()
#     return info


# def writeToJson(frienddict, friendlistUrl="friendlist.json"):
#     if frienddict:
#         with codecs.open(friendlistUrl, 'w', 'utf-8') as f:
#             f.write(json.dumps(frienddict, sort_keys=True,
#                                indent=4, ensure_ascii=False))
#     else:
#         print("Failed")



