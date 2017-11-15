
import asyncio
import aiohttp
import codecs
import time
import json
import re
import requests
from qzoneinfo import getInfo

class MsgList():
    """
    a class
    """
    @asyncio.coroutine
    async def getTwentyText(self,pos):
        url='https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6'
        self.params["pos"] = str(pos)
        async with aiohttp.ClientSession(cookies=self.cookies,headers=self.headers) as session:
            async with session.get(url, params=self.params) as resp:
                if resp and resp.status == 200:
                    data=await resp.text()
        data=data.replace("_preloadCallback(", '').replace(");", '').replace("_Callback(", '')
        return json.loads(data)


    def __init__(self, qqnumber):
        self.qqnumber = qqnumber
        self.hostqqnumber,self.cookies, self.gtk, self.g_qzonetoken = getInfo()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/61.0.3163.100 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        self.res_list = []
        self.params = {
            'uin': self.qqnumber,
            'ftype': '0',
            'sort': '0',
            'pos': '0',
            'num': '20',
            'replynum': '100',
            'callback': '_preloadCallback',
            'code_version': '1',
            'format': 'jsonp',
            'need_private_comment': '1',
            'g_tk': str(self.gtk),
            'qzonetoken': self.g_qzonetoken

        }
        self.likeParams={
            'uin':self.hostqqnumber,
            'unikey2':"http://user.qzone.qq.com/"+self.qqnumber+"/mood/",
            "g_tk":self.gtk,
            "qzonetoken":self.g_qzonetoken,
            'begin_uin': '0',
            'query_count': '60',
            'if_first_page': '1'
        }

        self.shuoshuolist = []

    def getone(self,text):
        """
        process one shuoshuo
        """
        one = {}
        one['id'] = text['tid']
        one["cmtnum"] = text["cmtnum"]
        commenttext = ''
        if "commentlist" in text.keys() and text["commentlist"] != None:
            for i in text["commentlist"]:
                commenttext = commenttext + i["content"] + ' '
                if "list_3" in i.keys():
                    for j in i["list_3"]:
                        commenttext = commenttext + j["content"] + ' '
        one["commentlist"] = self.process(commenttext)
        one["content"] = self.process(text["content"])
        one["created_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(text["created_time"]))
        if "rt_con" in text.keys():
            one["isTranferred"] = True
            one["TranferredContent"] = self.process(
                text["rt_con"].get("content"))
        return one

    def getNumber(self):
        self.params["pos"] = 0
        response = requests.get('https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
                                      params=self.params, headers=self.headers, cookies=self.cookies)
        if response and response.status_code == 200:
            text = response.text.replace(
                "_preloadCallback(", '').replace(");", '').replace("_Callback(", '')
            data = json.loads(text)
            print(self.qqnumber + " " + (data["message"] or "可以进入"))
            return data['usrinfo']['msgnum']


    def process(self, text):
        text = re.sub(r"\[em\].*?\[\/em\]", '', text)
        text = re.sub("\n", '', text)
        text = re.sub(r"@\{.*?\}", '', text)
        return text


    def main(self):
        event_loop = asyncio.get_event_loop()
        number=self.getNumber()
        tasks = [self.getTwentyText(pos*20) for pos in range(int(number/20)+1)]
        results = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()
        for i in results:
            for one in i['msglist']:
                self.shuoshuolist.append(self.getone(one))
        print("已完成%s的全部说说共%s个" % (self.qqnumber, len(self.shuoshuolist)))


if __name__ == "__main__":
    start = time.clock()
    my = MsgList('2539287124')
    my.main()
    with codecs.open("C:\\Personal Files\\projects\\qzone\\"+"2539287124.json",'w','utf-8') as f:
        f.write(json.dumps(my.shuoshuolist,sort_keys=True, indent=4,ensure_ascii=False))
    end = time.clock()
    print("用时" + str(end - start) + " s")
