import pickle
import codecs
import json
import requests
import re
import time
import os
from getQQFriendList import getInfo
from multiprocessing import Process


class GetMsgList():
    def __init__(self,qqnumber,infoUrl="qzoneInfo.txt"):
        self.qqnumber=qqnumber
        self.s=requests.session()
        self.cookie,self.gtk,self.g_qzonetoken=getInfo(infoUrl)
        self.headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                        'Accept': '*/*',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection':'keep-alive'
                        }
        self.params={
                        'uin':self.qqnumber,
                        'ftype':'0',
                        'sort':'0',
                        'pos':'0',
                        'num':'20',
                        'replynum':'100',
                        'callback':'_preloadCallback',
                        'code_version':'1',
                        'format':'jsonp',
                        'need_private_comment':'1',
                        'g_tk':str(self.gtk),
                        'qzonetoken':self.g_qzonetoken
                        }
        self.shuoshuolist=[]
        self.count=0
        self.pos=0
        self.over=False
    def getOne(self,text):
        one={}
        one['id']=str(text["uin"])+" "+text['tid']
        one["cmtnum"]=text["cmtnum"]
        commenttext=''
        if "commentlist" in text.keys() and text["commentlist"]!=None:
            for i in text["commentlist"]:
                commenttext=commenttext+i["content"]+' '
                if "list_3" in i.keys():
                    for j in i["list_3"]:
                        commenttext=commenttext+j["content"]+' '
        one["commentlist"]=self.process(commenttext)
        one["content"]=self.process(text["content"])
        one["created_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(text["created_time"]))
        if "rt_con" in text.keys():
            one["isTranferred"]=True
            one["TranferredContent"]=self.process(text["rt_con"].get("content"))
        else:
            one["isTranferred"]=False
            one["TranferredContent"]=''
        return one

    def getTwentyText(self):
        self.params["pos"]=str(self.pos)
        try:
            response=self.s.request('GET',
            'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
            params=self.params,headers=self.headers,cookies=self.cookie)
        except requests.exceptions.ConnectionError:
            print("Connected to network failed")
        if response and response.status_code==200:
            text=response.text.replace("_preloadCallback(",'').replace(");",'').replace("_Callback(",'')
        else:
            text=''
        return text

    def writetojson(self,jsonurl):
        if self.shuoshuolist:
            with codecs.open(jsonurl,'w','utf-8') as f:
                f.write(json.dumps(self.shuoshuolist,sort_keys=True, indent=4,ensure_ascii=False))
            print("write to json successfully")
        else:
            print("no shuoshuo to write")
        

    def process(self,text):
        text=re.sub("\[em\].*?\[\/em\]",'',text)
        text=re.sub("\n",'',text)
        text=re.sub("@\{.*?\}",'',text)
        return text

    def getAndMerge(self,text):
        data=json.loads(text)
        if self.count==0:
            print(self.qqnumber+" "+(data["message"] or "可以进入"))
        if 'msglist' not in data or data["msglist"]==None:
            self.over=True
        else:
            for i in data['msglist']:
                self.shuoshuolist.append(self.getOne(i))
                self.count=self.count+1
        
    def main(self,maxNumber=0):
        while self.count<(maxNumber or 2000) and not self.over:
            self.getAndMerge(self.getTwentyText())
            self.pos=self.pos+20

            
        print("已完成%s的全部说说共%s个" % (self.qqnumber,self.count))



if __name__=="__main__":
    my=GetMsgList('1255754523')
    my.main()


    
