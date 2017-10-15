import requests
import json
import pickle
import os

def testInfo(info):
    s=requests.session()
    cookies,gtk,g_qzonetoken=info
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection':'keep-alive'
    }
    params={
        'uin':'1255754523',
        'ftype':'0',
        'sort':'0',
        'pos':'0',
        'num':'20',
        'replynum':'100',
        'callback':'_preloadCallback',
        'code_version':'1',
        'format':'jsonp',
        'need_private_comment':'1',
        'g_tk':str(gtk),
        'qzonetoken':g_qzonetoken
        }
    try:
        response=s.request('GET',
        'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
        params=params,headers=headers,cookies=cookies)
    except requests.exceptions.ConnectionError:
        print("Connected to network failed")
    if response and response.status_code==200:
        text=response.text.replace("_preloadCallback(",'').replace(");",'').replace("_Callback(",'')
        data=json.loads(text)
        if data["message"]=="请先登录空间":
            return False
        else:
            return True
if __name__=="__main__":
    infoUrl="qzoneInfo.txt"
    if os.path.exists(infoUrl):
        with open(infoUrl,'rb') as f:
            if testInfo(pickle.load(f)):
                print("Cookie is valid")
            else:
                print("Cookie is not valid")
    else:
        print("no such file")
