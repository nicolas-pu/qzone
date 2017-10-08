"""
获取qq好友列表
"""

import pickle
import codecs
import json
import requests

f = open("info.txt", 'rb')
cookie, gtk, qzonetoken = pickle.load(f)
f.close()

s=requests.session()#用requests初始化会话
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
    'qzonetoken':qzonetoken}

s=requests.session()
response=s.request('GET',
    'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_hat_get.cgi',
    params=params,headers=headers,cookies=cookie)
print(response.status_code)
data=response.text
data=data.replace("_Callback(",'').replace(");",'')
jsondata=json.loads(data)

friend=jsondata.get("data")
if  friend==None:
    print("Cookie失效")
else:
    with codecs.open(r"friendlist.json",'w','utf-8') as f:
        f.write(json.dumps(jsondata,sort_keys=True, indent=4,ensure_ascii=False))
    for i in friend:
        if i != "activity":
            print(i+"  realname:"+jsondata['data'][i]['realname'])
