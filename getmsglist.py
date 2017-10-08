import pickle
import codecs
import json
import requests
import re
import time

def getcookie(qzoneCookieUrl):
    with open(qzoneCookieUrl,'rb') as f:
        cookie=pickle.load(f)
    return cookie


def getjson(qqnumber,pos,cookie,gtk,qzonetoken,session):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection':'keep-alive'
    }
    params={
        'uin':qqnumber,
        'ftype':'0',
        'sort':'0',
        'pos':str(pos),
        'num':'20',
        'replynum':'100',
        'callback':'_preloadCallback',
        'code_version':'1',
        'format':'jsonp',
        'need_private_comment':'1',
        'g_tk':str(gtk),
        'qzonetoken':qzonetoken
        }
    response=session.request('GET',
        'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
       params=params,headers=headers,cookies=cookie)
    if response.status_code==200:
        data=response.text.replace("_preloadCallback(",'').replace(");",'').replace("_Callback(",'')
    else:
        data=''
    return data

def writetojson(jsonurl,data):
    text=json.loads(data)
    try:
        with codecs.open(jsonurl,'w','utf-8') as f:
            f.write(json.dumps(text,sort_keys=True, indent=4,ensure_ascii=False))
        print("写入json成功")
    except:
        print("写入json失败")

def process(text):
    text=re.sub("\[em\].*?\[\/em\]",'',text)
    text=re.sub("\n",'',text)
    text=re.sub("@\{.*?\}",'',text)
    return text

def getshuoshuodict(data,shuoshuolist,count):
    text=json.loads(data)
    print(text["message"] or "可以进入")

    if 'msglist' not in text.keys() or text["msglist"]==None:
        return shuoshuolist,count
    else:
        for i in text['msglist']:
            shuoshuolist.append(getoneshuoshuodict(i))
            count=count+1
        print("完成说说共%s个" % count)
        return shuoshuolist,count
def getoneshuoshuodict(text):
    oneshuoshuodict={}
    oneshuoshuodict['id']=str(text["uin"])+" "+text['tid']
    oneshuoshuodict["cmtnum"]=text["cmtnum"]
    commenttext=''
    if "commentlist" in text.keys() and text["commentlist"]!=None:
        for i in text["commentlist"]:
            commenttext=commenttext+process(i["content"])+' '
            if "list_3" in i.keys():
                for j in i["list_3"]:
                    commenttext=commenttext+process(j["content"])+' '
    oneshuoshuodict["commentlist"]=commenttext
    oneshuoshuodict["content"]=process(text["content"])
    oneshuoshuodict["created_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(text["created_time"]))
    if "rt_con" in text.keys():
        oneshuoshuodict["isTranferred"]=True
        oneshuoshuodict["TranferredContent"]=process(text["rt_con"].get("content"))
    else:
        oneshuoshuodict["isTranferred"]=False
        oneshuoshuodict["TranferredContent"]=''
    return oneshuoshuodict
            
def main(qqnumber,qzoneCookieUrl):
    s=requests.session()
    wholeshuoshuolist=[]
    count=0
    for i in range(1):
        data=getjson(qqnumber,i*20,*getcookie(qzoneCookieUrl),s)
        while not data:
            data=getjson(qqnumber,i*20,*getcookie(qzoneCookieUrl),s)
        shuoshuolist,icount=getshuoshuodict(data,[],0)
        if shuoshuolist:
            for i in shuoshuolist:
                wholeshuoshuolist.append(i)
            count=count+icount
        else:
            print("已完成%s的全部说说共%s个" % (qqnumber,count))
            break
    return wholeshuoshuolist,count

if __name__=="__main__":
    main("1255754523","qzoneCookie.txt")

    
