
import asyncio
import codecs
import json
import time

import aiohttp
import requests

class LiuyanList():
    """
    a class
    """
    def __init__(self, qqnumber):
        self.qqnumber = qqnumber
        self.hostqqnumber, self.cookies, self.gtk, self.g_qzonetoken = prepare.INFO
        self.headers = prepare.headers
        self.params = {
            'uin': self.hostqqnumber,
            'hostUin': self.qqnumber,
            'format':'jsonp',
            'g_tk': str(self.gtk),
            'qzonetoken': self.g_qzonetoken,
            "inCharset":"utf-8",
            "num":"10",
            "outCharset":"utf-8"}
        self.liuyanlist = []


    @asyncio.coroutine
    async def get_ten_text(self, start):
        url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb'
        self.params["start"] = str(start)
        async with aiohttp.ClientSession(cookies=self.cookies, headers=self.headers) as session:
            async with session.get(url, params=self.params) as resp:
                if resp and resp.status == 200:
                    data = await resp.text()
                    data = data.replace("_preloadCallback(", '').replace(");", '').replace("_Callback(", '')
                    return json.loads(data)["data"]
                else:
                    return


    def get_number(self):
        self.params["start"] = 0
        response = requests.get('https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb',
                                params=self.params, headers=self.headers, cookies=self.cookies)
        if response and response.status_code == 200:
            text = response.text.replace(
                "_preloadCallback(", '').replace(");", '').replace("_Callback(", '')
            data = json.loads(text)
            print(self.qqnumber + " " + (data["message"] or "可以进入"))
            if data["message"]=="":
                return data['data']["total"]
            else:
                return 0

    def main(self):
        number = self.get_number()
        if number==0:
            print("%s 跳过" % (self.qqnumber))
            return
        event_loop = asyncio.get_event_loop()
        tasks = [self.get_ten_text(start * 10) for start in range(int(number / 10) + 1)]
        results = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()
        for i in results:
            for one in i['commentList']:
                self.liuyanlist.append(self.process_one(one))
        print("已完成%s的全部留言共%s个" % (self.qqnumber, len(self.liuyanlist)))

    @staticmethod
    def process_one(text):
        one = {"content": text["ubbContent"].replace("\n",""), "nickname": text["nickname"],
               "qqnumber":text["uin"],"time":text["pubtime"]}
        if "replyList" in text.keys() and text["replyList"] != []:
            one["replylist"]=[]
            for i in text["replyList"]:
                reply = {"content": i["content"], "name":i["nick"], "time": time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(i["time"]))}
                one["replylist"].append(reply)
        return one

if __name__ == "__main__":
    import prepare
    start = time.clock()
    my = LiuyanList('2481218301')
    my.main()
    with codecs.open("temp.json", 'w', 'utf-8') as f:
        f.write(json.dumps(my.liuyanlist, indent=2, ensure_ascii=False))
    end = time.clock()
    print("用时" + str(end - start) + " s")