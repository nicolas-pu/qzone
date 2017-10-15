"""
get QQ Friend list and write a dict to friendlist.json
"""

import pickle
import codecs
import json
import requests
from getQzoneCookie import getQzoneCookie
import os
from testInfo import testInfo

def getInfo(infoUrl):
    
    if os.path.exists(infoUrl):
        try:
            with open(infoUrl,'rb') as f:
                info=pickle.load(f)
        except pickle.UnpicklingError:
            info=getQzoneCookie(infoUrl)
        if testInfo(info):
            print("get cookie successfully")
        else:
            info=getQzoneCookie(infoUrl)
    else:
        info=getQzoneCookie(infoUrl)
    return info

def loginAndGetLsit(cookies,gtk,g_qzonetoken):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://user.qzone.qq.com/411029620?_t_=0.647450614322588',
        'Connection':'keep-alive'
    }
    params={
        'hat_seed':'1',
        'uin':'1255754523',
        'fupdate':'1',
        'g_tk':str(gtk),
        'qzonetoken':g_qzonetoken}
    try:
        s=requests.session()
        response=s.request('GET',
            'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_hat_get.cgi',
            params=params,headers=headers,cookies=cookies)
    except requests.exceptions.ConnectionError:
        print("Connected to network failed")
    frienddict={}
    if response:
        data=response.text.replace("_Callback(",'').replace(");",'')
        jsondata=json.loads(data)
        friend=jsondata.get("data")
        if  friend==None:
            print("Cookie login failed")
        else:
            print("Cookie login succeeded")
            for i in friend:
                if i != "activity":
                    frienddict[i]=friend[i]['realname']
    return frienddict

def writeToJson(frienddict,friendlistUrl):
    if frienddict:
        with codecs.open(friendlistUrl,'w','utf-8') as f:
            f.write(json.dumps(frienddict,sort_keys=True, indent=4,ensure_ascii=False))
    else:
        print("Failed")

def getQQFriendList(friendlistUrl,infoUrl="qzoneInfo.txt"):
    info=getInfo(infoUrl)
    frienddict=loginAndGetLsit(*info)
    print("get QQFriendList successful")
    writeToJson(frienddict,friendlistUrl)
    return frienddict
    

if __name__=="__main__":
    friendlistUrl="friendlist.json"
    infoUrl="qzoneInfo.txt"
    print(getQQFriendList(friendlistUrl,infoUrl))

